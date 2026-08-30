from rest_framework import serializers

from .models import Design, Forecast, Insight


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        exclude = ["design"]


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        exclude = ["design"]


class DesignSerializer(serializers.ModelSerializer):
    forecast = ForecastSerializer(read_only=True)
    insight = InsightSerializer(read_only=True)

    class Meta:
        model = Design
        fields = "__all__"

