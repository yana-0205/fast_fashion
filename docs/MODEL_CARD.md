# Model Card: Visuelle Statistical Baseline V1

## Purpose

Provide a deterministic, transparent ten-week demand forecast while the historical multimodal neural network is being recovered and independently validated.

## Method

For a new concept, the model selects historical records using the most specific available match:

1. Category, color, and fabric
2. Category and color
3. Category
4. Global fallback

The interactive product uses the mean raw weekly sales profile of matched records. The offline evaluation applies the same grouping strategy to the official normalized `stfore_train.csv` and evaluates against `stfore_test.csv`.

## Evaluation

Run:

```bash
python scripts/evaluate_baseline.py --root ./visuelle2 --output docs/baseline_metrics.json
```

The generated `baseline_metrics.json` is the source of truth for the current metrics.

Current V1 result on 96,166 training rows and 10,684 held-out test rows:

- MAE: 0.021086
- RMSE: 0.031155
- WAPE: 0.860063
- Exact category/color/fabric matches: 9,228 test records

The high WAPE confirms that this baseline should be treated as a reproducible lower bound and workflow fallback, not a production-quality forecasting model.

## Intended use

- Product workflow validation
- Explainable fallback forecast
- Benchmark for restored or newly trained models
- Early comparison between design concepts

## Limitations

- This is a similarity-based statistical baseline, not the original HMA-RNN.
- It does not infer causal effects of price or design changes.
- It does not yet extract visual embeddings from a newly generated image.
- Historical averages can underrepresent rare or breakout products.
- Interactive raw-unit results and normalized test metrics use different scales and must not be compared directly.
- Results support exploration and portfolio demonstration, not production inventory commitments.
