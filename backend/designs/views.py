from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Design, Forecast, Insight
from .serializers import DesignSerializer, ForecastSerializer, InsightSerializer
from .services import attach_dataset_image, build_template_insight, get_baseline


def health(_request):
    return JsonResponse({"status": "ok", "version": "v1"})


@api_view(["GET"])
def options(_request):
    return Response(get_baseline().options())


class DesignListCreateView(generics.ListCreateAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer


class DesignDetailView(generics.RetrieveDestroyAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer


@api_view(["POST"])
def generate_design(request):
    serializer = DesignSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    design = serializer.save()
    try:
        attach_dataset_image(design)
    except (FileNotFoundError, IndexError) as exc:
        design.delete()
        return Response(
            {"error": {"code": "DATASET_IMAGE_UNAVAILABLE", "message": str(exc), "details": {}}},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return Response(DesignSerializer(design).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def forecast_design(_request, pk):
    design = generics.get_object_or_404(Design, pk=pk)
    result = get_baseline().predict(design.category, design.color, design.fabric)
    forecast, _ = Forecast.objects.update_or_create(design=design, defaults=result)
    return Response(ForecastSerializer(forecast).data)


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
    return Response({"designs": DesignSerializer(designs, many=True).data})
