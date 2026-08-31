from django.http import JsonResponse
from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Design, Forecast, Insight
from .serializers import DesignSerializer, ForecastSerializer, InsightSerializer
from .services import PRODUCT_OPTIONS, build_template_insight, save_uploaded_design_image


def health(_request):
    return JsonResponse({"status": "ok", "version": "v1"})


@api_view(["GET"])
def dashboard(_request):
    designs = Design.objects.select_related("forecast").all()
    total_designs = designs.count()
    forecasted = designs.filter(forecast__isnull=False)
    top_design = forecasted.order_by("-forecast__total_forecast").first()
    recent = designs[:4]
    return Response(
        {
            "total_designs": total_designs,
            "forecasted_designs": forecasted.count(),
            "average_total_forecast": round(
                forecasted.aggregate(value=Avg("forecast__total_forecast"))["value"] or 0,
                2,
            ),
            "top_design": DesignSerializer(top_design).data if top_design else None,
            "recent_designs": DesignSerializer(recent, many=True).data,
        }
    )


@api_view(["GET"])
def options(_request):
    return Response(PRODUCT_OPTIONS)


class DesignListCreateView(generics.ListCreateAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer


class DesignDetailView(generics.RetrieveDestroyAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer


@api_view(["POST"])
def generate_design(request):
    uploaded_image = request.FILES.get("image")
    if uploaded_image is None:
        return Response(
            {"error": {"code": "DESIGN_IMAGE_REQUIRED", "message": "Upload a design image.", "details": {}}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = DesignSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    design = serializer.save()
    try:
        save_uploaded_design_image(design, uploaded_image)
    except OSError as exc:
        design.delete()
        return Response(
            {"error": {"code": "IMAGE_SAVE_FAILED", "message": str(exc), "details": {}}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(DesignSerializer(design).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def forecast_design(_request, pk):
    generics.get_object_or_404(Design, pk=pk)
    return Response(
        {
            "error": {
                "code": "FORECAST_MODEL_UNAVAILABLE",
                "message": "A trained forecast model artifact has not been configured yet.",
                "details": {},
            }
        },
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


@api_view(["POST"])
def insight_design(_request, pk):
    design = generics.get_object_or_404(Design, pk=pk)
    if not hasattr(design, "forecast"):
        return Response(
            {"error": {"code": "FORECAST_REQUIRED", "message": "Run a forecast first.", "details": {}}},
            status=status.HTTP_409_CONFLICT,
        )
    payload = build_template_insight(design, ForecastSerializer(design.forecast).data)
    insight, _ = Insight.objects.update_or_create(design=design, defaults=payload)
    return Response(InsightSerializer(insight).data)


@api_view(["POST"])
def compare_designs(request):
    ids = request.data.get("design_ids", [])
    if not isinstance(ids, list) or len(ids) != 2 or ids[0] == ids[1]:
        return Response(
            {"error": {"code": "EXACTLY_TWO_DESIGNS_REQUIRED", "message": "Choose two different designs.", "details": {}}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    designs = list(Design.objects.filter(pk__in=ids).select_related("forecast", "insight"))
    if len(designs) != 2:
        return Response(
            {"error": {"code": "DESIGN_NOT_FOUND", "message": "One or more designs do not exist.", "details": {}}},
            status=status.HTTP_404_NOT_FOUND,
        )
    forecasted = [design for design in designs if hasattr(design, "forecast")]
    recommendation = None
    if len(forecasted) == 2:
        winner = max(forecasted, key=lambda item: item.forecast.total_forecast)
        other = min(forecasted, key=lambda item: item.forecast.total_forecast)
        difference = winner.forecast.total_forecast - other.forecast.total_forecast
        if abs(difference) < 1e-9:
            recommendation = {
                "winner_id": None,
                "summary": "两个方案的当前基线累计预测相同，应结合差异化程度、价格和目标客群继续判断。",
                "basis": "ten_week_total_tie",
            }
        else:
            recommendation = {
                "winner_id": winner.id,
                "summary": f"{winner.title} 的十周累计预测高出 {difference:.1f} 件，当前基线更支持该方案。",
                "basis": "higher_ten_week_total",
            }
    return Response({"designs": DesignSerializer(designs, many=True).data, "recommendation": recommendation})
