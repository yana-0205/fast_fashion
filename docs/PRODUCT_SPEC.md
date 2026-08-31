# V1 Product Specification

## Product goal

Help a fast-fashion designer or merchandise planner create a womenswear concept and evaluate its expected ten-week demand before committing to production.

## Primary workflow

1. Select category, color, fabric, season, and price.
2. Add optional positive and negative design descriptions.
3. Generate an image through a configured provider or upload a design image.
4. Forecast ten weeks of sales.
5. Review color, fabric, season, and price insights.
6. Save the concept and compare it with one alternative.

## V1 features

- Design concept creation
- User-uploaded design image
- Pluggable text-to-image provider boundary
- Ten-week sales forecast
- Market insight report
- Saved design portfolio
- Two-design comparison

## Explicit non-goals

- Admin portal and enterprise management
- Authentication and multi-tenant permissions
- Dataset management UI
- Production queues or high-concurrency infrastructure
- Mandatory 3D generation
- Agent-driven product behavior

## Acceptance criteria

- Design creation works without external API keys through image upload.
- Forecasting is enabled only when a validated model artifact is configured.
- Forecasts contain exactly ten finite, non-negative values when the model is available.
- Forecast output identifies model version and evaluation metrics.
- The application distinguishes model output, data statistics, and generated explanation.
- Visuelle 2.0 is used only by offline training and evaluation workflows.
- A clean checkout can be started by following the README.
