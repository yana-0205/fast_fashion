import argparse
import json
from pathlib import Path

import pandas as pd
from PIL import Image

REQUIRED_SALES_COLUMNS = {
    "external_code",
    "retail",
    "season",
    "category",
    "color",
    "image_path",
    "fabric",
    "release_date",
    "restock",
    *map(str, range(12)),
}


def validate(root: Path, image_sample: int = 100) -> dict:
    sales_path = root / "sales.csv"
    images_root = root / "images"
    if not sales_path.is_file():
        raise FileNotFoundError(f"Missing required file: {sales_path}")
    if not images_root.is_dir():
        raise FileNotFoundError(f"Missing image directory: {images_root}")

    sales = pd.read_csv(sales_path)
    missing_columns = sorted(REQUIRED_SALES_COLUMNS - set(sales.columns))
    sample = sales.head(image_sample)
    missing_images = []
    invalid_images = []
    for relative_path in sample["image_path"].dropna():
        image_path = images_root / relative_path
        if not image_path.is_file():
            missing_images.append(str(relative_path))
            continue
        try:
            with Image.open(image_path) as image:
                image.verify()
        except Exception:
            invalid_images.append(str(relative_path))

    return {
        "rows": int(len(sales)),
        "columns": int(len(sales.columns)),
        "missing_required_columns": missing_columns,
        "categories": int(sales["category"].nunique()),
        "colors": int(sales["color"].nunique()),
        "fabrics": int(sales["fabric"].nunique()),
        "sampled_images": int(len(sample)),
        "missing_images": missing_images,
        "invalid_images": invalid_images,
        "valid": not missing_columns and not missing_images and not invalid_images,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--image-sample", type=int, default=100)
    args = parser.parse_args()
    report = validate(args.root, args.image_sample)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()

