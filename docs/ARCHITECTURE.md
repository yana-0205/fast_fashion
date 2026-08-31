# V1 Architecture

## Product flow

```text
React workspace
  -> Django REST API
     -> Design persistence (SQLite)
     -> Image upload / text-to-image provider
     -> Exported ten-week forecast model artifact
     -> Deterministic insight provider
```

## Boundaries

- `frontend/` owns interaction and visualization.
- `backend/designs/` owns API contracts and persistence.
- `ml/` owns offline training, evaluation, artifact export, and runtime inference contracts.
- `visuelle2/` is an offline training dependency and is never read by the product runtime.
- External image and language model providers are optional future adapters, not requirements for V1.

## Data boundary

Visuelle 2.0 belongs exclusively to model development: preprocessing, training, validation, and artifact export. The Django product runtime consumes only the exported model artifact and its preprocessing metadata. It never queries the training dataset to manufacture an online prediction.

Design images come from user upload or a separately configured text-to-image provider. Market analysis must identify its own source and cannot relabel training-data statistics as current market intelligence.
