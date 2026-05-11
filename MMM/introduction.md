1. Data validation
   - check missing dates
   - check negative spend
   - check duplicate dates
   - check impossible GMV / units / MRP values

2. Reproducible pipeline
   - one script or pipeline for:
     raw data → clean data → features → model → ROI output

3. Time-series validation
   - rolling-window validation, not only one train/test split

4. Hyperparameter tuning
   - tune adstock decay
   - tune saturation alpha
   - tune Ridge/Lasso/ElasticNet parameters

5. Coefficient sanity checks
   - media coefficients should usually be positive
   - ROI should be realistic
   - contribution should not exceed total sales unrealistically

6. Model diagnostics
   - residual plot
   - actual vs predicted plot
   - error over time
   - seasonality not captured by model

7. Experiment validation
   - compare MMM results with A/B tests, geo-lift tests, or campaign holdouts if possible

8. Artifact versioning
   - save model version
   - feature version
   - data date range
   - metrics
   - assumptions

9. Dashboard
   - channel contribution
   - ROI
   - actual vs predicted
   - recommended budget shift

10. Monitoring and refresh
   - rerun weekly/monthly
   - track drift in spend and sales
   - retrain when performance drops