# Fast Fashion Design & Demand Forecasting

Portfolio-oriented reconstruction of a fast-fashion womenswear design and demand forecasting platform. V1 preserves the original product intent while rebuilding the workflow, interface, forecasting boundary, and engineering structure.

## What it does

- Builds a womenswear concept from category, color, fabric, season, price, and design notes
- Matches a real Visuelle 2.0 reference image when no external image API is configured
- Forecasts the next ten weeks from similar historical product profiles
- Separates statistical output from deterministic narrative insights
- Saves concepts and compares two forecast curves side by side

## V1 workflow

Create a design concept, obtain a dataset-matched image, forecast ten weeks of sales, review market insights, save the concept, and compare two concepts.

## Model status

V1 currently uses an explainable statistical lower-bound model. On the official normalized split it reports MAE 0.021086, RMSE 0.031155, and WAPE 0.860063. The high WAPE is documented deliberately: this model validates the workflow and provides a reproducible fallback, but it is not presented as production-quality demand forecasting.

See `docs/MODEL_CARD.md` and `docs/baseline_metrics.json`.

## Local setup

### Backend

Python 3.9 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Dataset validation

The full `visuelle2` directory is intentionally excluded from Git.

```bash
python scripts/validate_dataset.py --root ./visuelle2
```

Evaluate the baseline:

```bash
python scripts/evaluate_baseline.py --root ./visuelle2 --output docs/baseline_metrics.json
```

## API

```text
GET    /api/options/
POST   /api/designs/generate/
GET    /api/designs/
GET    /api/designs/{id}/
DELETE /api/designs/{id}/
POST   /api/designs/{id}/forecast/
POST   /api/designs/{id}/insights/
POST   /api/designs/compare/
GET    /api/health/
```

## Reproduction policy

This is a functional reconstruction and product redesign, not a pixel-for-pixel copy of the historical graduation project. Product intent and core capabilities are preserved; low-value administration screens and fragile infrastructure are deferred. The product itself is not Agent-driven. Agent/Codex usage belongs to the development-learning record only.

See `docs/PRODUCT_SPEC.md`, `docs/REPRODUCTION_SCOPE.md`, and `docs/ARCHITECTURE.md`.
