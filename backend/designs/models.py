from django.db import models


class Design(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    color = models.CharField(max_length=80)
    fabric = models.CharField(max_length=80)
    season = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    prompt = models.TextField(blank=True)
    negative_prompt = models.TextField(blank=True)
    image_path = models.CharField(max_length=500, blank=True)
    image_source = models.CharField(max_length=40, default="dataset")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Forecast(models.Model):
    design = models.OneToOneField(Design, on_delete=models.CASCADE, related_name="forecast")
    weekly_forecast = models.JSONField()
    total_forecast = models.FloatField()
    peak_week = models.PositiveSmallIntegerField()
    peak_sales = models.FloatField()
    risk_level = models.CharField(max_length=20)
    model_version = models.CharField(max_length=80)
    metrics = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class Insight(models.Model):
    design = models.OneToOneField(Design, on_delete=models.CASCADE, related_name="insight")
    color_analysis = models.TextField()
    fabric_analysis = models.TextField()
    season_analysis = models.TextField()
    price_analysis = models.TextField()
    summary = models.TextField()
    source = models.CharField(max_length=40, default="template")
    created_at = models.DateTimeField(auto_now_add=True)

