from django.urls import path

from .views import (
    DesignDetailView,
    DesignListCreateView,
    compare_designs,
    dashboard,
    forecast_design,
    generate_design,
    insight_design,
    market_trends,
    options,
)

urlpatterns = [
    path("dashboard/", dashboard),
    path("options/", options),
    path("market-trends/", market_trends),
    path("designs/generate/", generate_design),
    path("designs/compare/", compare_designs),
    path("designs/", DesignListCreateView.as_view()),
    path("designs/<int:pk>/forecast/", forecast_design),
    path("designs/<int:pk>/insights/", insight_design),
    path("designs/<int:pk>/", DesignDetailView.as_view()),
]
