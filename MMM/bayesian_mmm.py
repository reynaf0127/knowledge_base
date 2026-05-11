import numpy as np
import pandas as pd
from pathlib import Path
from joblib import load

from lightweight_mmm import lightweight_mmm
from lightweight_mmm import preprocessing
from lightweight_mmm import plot
from lightweight_mmm import optimize_media

from sklearn.metrics import r2_score, mean_absolute_error


# -----------------------------
# 1. Load your MMM dataset
# -----------------------------
df = pd.read_csv('./MMM/data/merge_df.csv')

# Make sure date is datetime
df["Date_"] = pd.to_datetime(df["Date_"])

df = df.sort_values("Date_").reset_index(drop=True)
# -----------------------------
# 2. Define target, media, controls
# -----------------------------
target_col = "total_gmv_"

media_cols = [
    "tv",
    "digital",
    "sponsorship",
    "content_marketing",
    "online_marketing",
    "affiliates",
    "sem",
    "radio",
    "other"
]

control_cols = [
    "total_discount_",
    "bed",
    "bsd_5",
    "big_diwali_sale",
    "christmas_new_year_sale",
    "daussera_sale",
    "eid_rathayatra_sale",
    "fhsd",
    "independence_sale",
    "pacman",
    "rakshabandhan_sale",
    "republic_day",
    "valentine_s_day"
]

# Keep only controls that exist
control_cols = [col for col in control_cols if col in df.columns]
# -----------------------------
# 3. Clean data
# -----------------------------
cols_needed = [target_col] + media_cols + control_cols

df[cols_needed] = (
    df[cols_needed]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
)

# Optional: log target if GMV has huge spikes
# LightweightMMM expects a numeric target.
# You can try both raw GMV and log GMV.
df["log_gmv"] = np.log1p(df[target_col])
target_col = "log_gmv"
# -----------------------------
# 4. Build arrays
# -----------------------------
media_data = df[media_cols].values
target = df[target_col].values
extra_features = df[control_cols].values if control_cols else None
# media_prior usually reflects spend share.
# A common starting point is total spend per channel.
media_prior = df[media_cols].sum().values
# Avoid zeros in prior
media_prior = np.where(media_prior == 0, 1, media_prior)
# -----------------------------
# 5. Time-series train/test split
# -----------------------------
split_idx = int(len(df) * 0.8)

media_train = media_data[:split_idx]
media_test = media_data[split_idx:]

target_train = target[:split_idx]
target_test = target[split_idx:]

if extra_features is not None:
    extra_train = extra_features[:split_idx]
    extra_test = extra_features[split_idx:]
else:
    extra_train = None
    extra_test = None
# -----------------------------
# 6. Scale data
# LightweightMMM recommends scaling media, target, extra features.
# -----------------------------
media_scaler = preprocessing.CustomScaler(divide_operation=np.mean)
target_scaler = preprocessing.CustomScaler(divide_operation=np.mean)

media_train_scaled = media_scaler.fit_transform(media_train)
media_test_scaled = media_scaler.transform(media_test)

target_train_scaled = target_scaler.fit_transform(target_train)
target_test_scaled = target_scaler.transform(target_test)

if extra_train is not None:
    extra_scaler = preprocessing.CustomScaler(divide_operation=np.mean)
    extra_train_scaled = extra_scaler.fit_transform(extra_train)
    extra_test_scaled = extra_scaler.transform(extra_test)
else:
    extra_scaler = None
    extra_train_scaled = None
    extra_test_scaled = None

# Scale media prior too
media_prior_scaled = media_prior / media_prior.mean()
# -----------------------------
# 7. Fit Bayesian MMM
# model_name options:
# "hill_adstock", "adstock", "carryover"
# -----------------------------
mmm = lightweight_mmm.LightweightMMM(model_name="hill_adstock")

mmm.fit(
    media=media_train_scaled,
    media_prior=media_prior_scaled,
    target=target_train_scaled,
    extra_features=extra_train_scaled,
    number_warmup=1000,
    number_samples=1000,
    number_chains=2,
    weekday_seasonality=True,
    seasonality_frequency=365,
    seed=42
)
# -----------------------------
# 8. Predict test period
# -----------------------------
prediction_scaled = mmm.predict(
    media=media_test_scaled,
    extra_features=extra_test_scaled,
    target_scaler=target_scaler
)
# prediction can be posterior samples.
# Take mean prediction.
if len(prediction_scaled.shape) > 1:
    y_pred = np.mean(prediction_scaled, axis=0)
else:
    y_pred = prediction_scaled

y_true = target_test
print("Test R2:", r2_score(y_true, y_pred))
print("Test MAE:", mean_absolute_error(y_true, y_pred))
# -----------------------------
# 9. Save prediction output
# -----------------------------
output_dir = Path("./mmm_outputs/bayesian_mmm")
output_dir.mkdir(parents=True, exist_ok=True)

pred_df = pd.DataFrame({
    "date": df["Date_"].iloc[split_idx:].values,
    "actual": y_true,
    "predicted": y_pred
})

pred_df.to_csv(output_dir / "bayesian_predictions.csv", index=False)


# -----------------------------
# 10. Plot model diagnostics
# -----------------------------
plot.plot_model_fit(
    media_mix_model=mmm,
    target_scaler=target_scaler
)

plot.plot_media_channel_posteriors(media_mix_model=mmm)

plot.plot_prior_and_posterior(media_mix_model=mmm)


# -----------------------------
# 11. Media contribution / ROI
# -----------------------------
media_contribution, roi_hat = mmm.get_posterior_metrics(
    target_scaler=target_scaler,
    cost_scaler=media_scaler
)

# contribution and ROI are posterior distributions.
# Take posterior means.
contribution_mean = np.mean(media_contribution, axis=0)
roi_mean = np.mean(roi_hat, axis=0)

roi_df = pd.DataFrame({
    "channel": media_cols,
    "roi": roi_mean
}).sort_values("roi", ascending=False)

roi_df.to_csv(output_dir / "bayesian_channel_roi.csv", index=False)

print(roi_df)


# -----------------------------
# 12. Budget optimization
# -----------------------------
# Use average historical spend as baseline budget.
prices = np.ones(len(media_cols))

budget = df[media_cols].sum().sum()

solution = optimize_media.find_optimal_budgets(
    n_time_periods=30,
    media_mix_model=mmm,
    budget=budget,
    prices=prices,
    media_scaler=media_scaler,
    target_scaler=target_scaler,
    extra_features=extra_train_scaled[-30:] if extra_train_scaled is not None else None,
    seed=42
)

print("Budget optimization result:")
print(solution)