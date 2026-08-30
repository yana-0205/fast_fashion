import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.baseline import FORECAST_WEEKS  # noqa: E402


def evaluate(dataset_root: Path) -> dict:
    train = pd.read_csv(dataset_root / "stfore_train.csv")
    test = pd.read_csv(dataset_root / "stfore_test.csv")
    keys = ["category", "color", "fabric"]
    global_profile = train[FORECAST_WEEKS].mean().to_numpy(dtype=float)

    profiles = {
        tuple(row[key] for key in keys): row[FORECAST_WEEKS].to_numpy(dtype=float)
        for _, row in train.groupby(keys, dropna=False)[FORECAST_WEEKS].mean().reset_index().iterrows()
    }
    category_color_profiles = {
        (row["category"], row["color"]): row[FORECAST_WEEKS].to_numpy(dtype=float)
        for _, row in train.groupby(["category", "color"], dropna=False)[FORECAST_WEEKS].mean().reset_index().iterrows()
    }
    category_profiles = {
        row["category"]: row[FORECAST_WEEKS].to_numpy(dtype=float)
        for _, row in train.groupby("category", dropna=False)[FORECAST_WEEKS].mean().reset_index().iterrows()
    }

    predictions = []
    levels = {"category+color+fabric": 0, "category+color": 0, "category": 0, "global": 0}
    for row in test.itertuples(index=False):
        exact_key = (row.category, row.color, row.fabric)
        pair_key = (row.category, row.color)
        if exact_key in profiles:
            prediction, level = profiles[exact_key], "category+color+fabric"
        elif pair_key in category_color_profiles:
            prediction, level = category_color_profiles[pair_key], "category+color"
        elif row.category in category_profiles:
            prediction, level = category_profiles[row.category], "category"
        else:
            prediction, level = global_profile, "global"
        predictions.append(prediction)
        levels[level] += 1

    predicted = np.vstack(predictions)
    actual = test[FORECAST_WEEKS].to_numpy(dtype=float)
    absolute_error = np.abs(predicted - actual)
    mae = float(absolute_error.mean())
    rmse = float(np.sqrt(np.mean((predicted - actual) ** 2)))
    denominator = float(np.abs(actual).sum())
    wape = float(absolute_error.sum() / denominator) if denominator else None
    return {
        "model_version": "visuelle-statistical-baseline-v1",
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "forecast_horizon": len(FORECAST_WEEKS),
        "metrics": {"mae": round(mae, 6), "rmse": round(rmse, 6), "wape": round(wape, 6) if wape is not None else None},
        "match_levels": levels,
        "data_scale": "normalized Visuelle 2.0 stfore split",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate(args.root)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

