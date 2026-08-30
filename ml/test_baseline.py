from pathlib import Path

from ml.baseline import StatisticalForecastBaseline


def test_baseline_returns_ten_finite_non_negative_values():
    model = StatisticalForecastBaseline(Path("visuelle2"))
    result = model.predict("long sleeve", "grey", "acrylic")
    assert len(result["weekly_forecast"]) == 10
    assert all(value >= 0 for value in result["weekly_forecast"])
    assert result["peak_week"] in range(1, 11)

