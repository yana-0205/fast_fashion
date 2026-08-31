# Forecast Model Card

## Purpose

Track the trained ten-week multimodal demand forecasting artifact used by the product runtime.

## Current status

No production inference artifact is configured yet. The API intentionally returns `FORECAST_MODEL_UNAVAILABLE` instead of manufacturing a prediction from training-set neighbors or historical averages.

## Intended training inputs

- Product image features
- Category, color, fabric, and season labels
- Historical and exogenous time-series features defined by the training experiment
- Ten-week sales target

## Required artifact contract

- Model weights
- Label vocabularies
- Feature normalization parameters
- Image preprocessing configuration
- Forecast horizon and output scale
- Training data version
- Held-out evaluation metrics

## Intended use

- Forecast future ten-week demand for a user-supplied or generated design
- Compare candidate designs using outputs from the same validated artifact

## Limitations

- The model must not be used before held-out evaluation is completed.
- Predictions do not establish causal effects of price or design changes.
- Results support design decisions but do not constitute inventory guarantees.
