# V1 Architecture

## Product flow

```text
React workspace
  -> Django REST API
     -> Design persistence (SQLite)
     -> Visuelle image matcher
     -> Ten-week forecast provider
     -> Deterministic insight provider
```

## Boundaries

- `frontend/` owns interaction and visualization.
- `backend/designs/` owns API contracts and persistence.
- `ml/` owns forecasting and dataset matching logic.
- `visuelle2/` is a local data dependency and is never committed.
- External image and language model providers are optional future adapters, not requirements for V1.

## Offline-first behavior

V1 deliberately completes its entire workflow without API credentials. Attribute selection is matched to a real Visuelle 2.0 product image, forecasting uses historical sales profiles, and insights use deterministic templates. This makes failures explicit and the project reproducible.

