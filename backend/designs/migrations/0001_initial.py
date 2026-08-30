from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Design",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("category", models.CharField(max_length=80)),
                ("color", models.CharField(max_length=80)),
                ("fabric", models.CharField(max_length=80)),
                ("season", models.CharField(max_length=40)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("prompt", models.TextField(blank=True)),
                ("negative_prompt", models.TextField(blank=True)),
                ("image_path", models.CharField(blank=True, max_length=500)),
                ("image_source", models.CharField(default="dataset", max_length=40)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Forecast",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("weekly_forecast", models.JSONField()),
                ("total_forecast", models.FloatField()),
                ("peak_week", models.PositiveSmallIntegerField()),
                ("peak_sales", models.FloatField()),
                ("risk_level", models.CharField(max_length=20)),
                ("model_version", models.CharField(max_length=80)),
                ("metrics", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("design", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="forecast", to="designs.design")),
            ],
        ),
        migrations.CreateModel(
            name="Insight",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("color_analysis", models.TextField()),
                ("fabric_analysis", models.TextField()),
                ("season_analysis", models.TextField()),
                ("price_analysis", models.TextField()),
                ("summary", models.TextField()),
                ("source", models.CharField(default="template", max_length=40)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("design", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="insight", to="designs.design")),
            ],
        ),
    ]

