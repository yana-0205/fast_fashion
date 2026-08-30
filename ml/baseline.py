from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

FORECAST_WEEKS = [str(index) for index in range(10)]


class StatisticalForecastBaseline:
    """Transparent fallback using matched Visuelle 2.0 sales profiles."""

    def __init__(self, dataset_root: Path):
        self.dataset_root = Path(dataset_root)
        self.sales = self._load(self.dataset_root)

    @staticmethod
    @lru_cache(maxsize=2)
    def _load(dataset_root: Path) -> pd.DataFrame:
        path = dataset_root / "sales.csv"
        if not path.is_file():
            raise FileNotFoundError(f"Missing raw sales data: {path}")
        return pd.read_csv(path)

    def _matched_rows(self, category: str, color: str, fabric: str) -> tuple[pd.DataFrame, str]:
        candidates = self.sales
        levels = [
            (["category", "color", "fabric"], "category+color+fabric"),
            (["category", "color"], "category+color"),
            (["category"], "category"),
        ]
        values = {"category": category, "color": color, "fabric": fabric}
        for columns, label in levels:
            mask = pd.Series(True, index=candidates.index)
            for column in columns:
                mask &= candidates[column].str.lower() == values[column].lower()
            matched = candidates.loc[mask]
            if len(matched) >= 5:
                return matched, label
        return candidates, "global"

    def predict(self, category: str, color: str, fabric: str) -> dict:
        matched, match_level = self._matched_rows(category, color, fabric)
        weekly = matched[FORECAST_WEEKS].mean(axis=0).to_numpy(dtype=float)
        weekly = np.nan_to_num(weekly, nan=0.0, posinf=0.0, neginf=0.0)
        weekly = np.clip(weekly, 0.0, None)
        peak_index = int(np.argmax(weekly))
        coefficient_of_variation = float(weekly.std() / (weekly.mean() + 1e-8))
        risk = "high" if coefficient_of_variation > 0.8 else "medium" if coefficient_of_variation > 0.4 else "low"
        return {
            "weekly_forecast": [round(float(value), 4) for value in weekly],
            "total_forecast": round(float(weekly.sum()), 4),
            "peak_week": peak_index + 1,
            "peak_sales": round(float(weekly[peak_index]), 4),
            "risk_level": risk,
            "model_version": "visuelle-statistical-baseline-v1",
            "metrics": {
                "matched_records": int(len(matched)),
                "match_level": match_level,
                "sales_scale": "raw_units",
            },
        }

    def options(self) -> dict:
        return {
            "categories": sorted(self.sales["category"].dropna().unique().tolist()),
            "colors": sorted(self.sales["color"].dropna().unique().tolist()),
            "fabrics": sorted(self.sales["fabric"].dropna().unique().tolist()),
            "seasons": ["spring-summer", "autumn-winter"],
        }

    def market_trends(self, limit: int = 8) -> dict:
        weekly = self.sales[[str(index) for index in range(10)]].mean(axis=0)

        def ranked(field: str) -> list[dict]:
            grouped = (
                self.sales.groupby(field, dropna=False)
                .agg(products=(field, "size"), average_sales=("0", "mean"))
                .reset_index()
                .sort_values(["products", "average_sales"], ascending=False)
                .head(limit)
            )
            return [
                {
                    "name": str(row[field]),
                    "products": int(row["products"]),
                    "average_sales": round(float(row["average_sales"]), 3),
                }
                for _, row in grouped.iterrows()
            ]

        return {
            "dataset_rows": int(len(self.sales)),
            "categories": ranked("category"),
            "colors": ranked("color"),
            "fabrics": ranked("fabric"),
            "weekly_average": [
                {"week": index + 1, "sales": round(float(value), 3)}
                for index, value in enumerate(weekly)
            ],
            "source": "Visuelle 2.0 raw sales.csv",
        }

    def match_image(self, category: str, color: str, fabric: str) -> Path:
        matched, _ = self._matched_rows(category, color, fabric)
        relative_path = matched.iloc[0]["image_path"]
        return self.dataset_root / "images" / relative_path
