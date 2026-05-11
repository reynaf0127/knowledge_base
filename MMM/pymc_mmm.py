import pandas as pd
import numpy as np
from joblib import load
from pathlib import Path

from pymc_marketing.mmm import GeometricAdstock, LogisticSaturation
from pymc_marketing.mmm.multidimensional import MMM
from sklearn.metrics import r2_score, mean_absolute_error


# -----------------------------
# 1. Load data
# -----------------------------
df = pd.read_csv('./MMM/data/merge_df.csv')

# clean column names just in case
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[ &\-]+", "_", regex=True)
    .str.replace(r"_+", "_", regex=True)
)

# rename date / target if needed
df = df.rename(columns={
    "date_": "date",
    "total_gmv_": "total_gmv",
    "total_discount_": "total_discount"
})

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)


# -----------------------------
# 2. Define columns
# -----------------------------
# optional: use log target if GMV has huge spikes
df["log_gmv"] = np.log1p(df['total_gmv'])
target_col = "log_gmv"

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
    "total_discount",
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

# keep only existing columns
media_cols = [c for c in media_cols if c in df.columns]
control_cols = [c for c in control_cols if c in df.columns]


# -----------------------------
# 3. Clean values
# -----------------------------
needed_cols = ["date", target_col] + media_cols + control_cols

df = df[needed_cols].copy()
df = df.replace([np.inf, -np.inf], np.nan)
df[media_cols + control_cols + [target_col]] = df[media_cols + control_cols + [target_col]].fillna(0)

# -----------------------------
# 4. Train/test split by time
# -----------------------------
split_idx = int(len(df) * 0.8)

train_df = df.iloc[:split_idx].copy()
test_df = df.iloc[split_idx:].copy()

X_train = train_df[["date"] + media_cols + control_cols]
y_train = train_df[target_col]

X_test = test_df[["date"] + media_cols + control_cols]
y_test = test_df[target_col]


# -----------------------------
# 5. Build Bayesian MMM
# -----------------------------
mmm = MMM(
    date_column="date",
    channel_columns=media_cols,
    control_columns=control_cols,
    target_column=target_col,
    adstock=GeometricAdstock(l_max=14),
    saturation=LogisticSaturation(),
    yearly_seasonality=2,
)


# -----------------------------
# 6. Fit model
# -----------------------------
idata = mmm.fit(
    X=X_train,
    y=y_train,
    draws=1000, # randomly select 1000 samples, then model have 1000 coef sets
    tune=1000, # first 10000 iteration will be disgarded. sample early guess are not stable, tuning help improve convergence and reduce bad sampling
    chains=2, # run 2 independent samples, 1000 draws per chain, total 2000 draws, all chains converge to sample region, detect stability
    target_accept=0.9, # 0.9 is safer, how conservative proposals (what if TV coef =0.6 etc) are 
    random_seed=42,
)

# -----------------------------
# 7. Predict
# -----------------------------
posterior_pred = mmm.predict(X_test)
pred_arr = np.asarray(posterior_pred)

print("prediction shape:", pred_arr.shape)

# Case 1: already one prediction per row
if pred_arr.ndim == 1:
    y_pred = pred_arr

# Case 2: posterior samples x observations
elif pred_arr.ndim == 2:
    # choose axis that matches len(y_test)
    if pred_arr.shape[0] == len(y_test):
        y_pred = pred_arr.mean(axis=1)
    elif pred_arr.shape[1] == len(y_test):
        y_pred = pred_arr.mean(axis=0)
    else:
        raise ValueError(f"Cannot align prediction shape {pred_arr.shape} with y_test length {len(y_test)}")

# Case 3: chain x draw x observations
elif pred_arr.ndim == 3:
    y_pred = pred_arr.mean(axis=(0, 1))

else:
    raise ValueError(f"Unexpected prediction shape: {pred_arr.shape}")

print("y_test length:", len(y_test))
print("y_pred shape:", y_pred.shape)

print("Test R2:", r2_score(y_test, y_pred))
print("Test MAE:", mean_absolute_error(y_test, y_pred))


# -----------------------------
# 8. Save model object + outputs
# -----------------------------
output_dir = Path("./MMM/output")
output_dir.mkdir(parents=True, exist_ok=True)

pred_df = pd.DataFrame({
    "date": test_df["date"],
    "actual": y_test,
    "predicted": y_pred
})

pred_df.to_csv(output_dir / "pymc_predictions.csv", index=False)

# Save inference data
idata.to_netcdf(output_dir / "pymc_mmm_trace.nc")

print("Saved outputs to:", output_dir)

### calcualte r_hat measure convergence chains
def calculate_rhat(chains):
    """
    chains shape:
    (n_chains, n_samples)

    Example:
    chains[0] = samples from chain 1
    chains[1] = samples from chain 2
    """

    chains = np.array(chains)

    m = chains.shape[0]  # number of chains
    n = chains.shape[1]  # samples per chain

    # -----------------------------
    # 1. Mean of each chain
    # -----------------------------
    chain_means = np.mean(chains, axis=1)

    # -----------------------------
    # 2. Overall mean
    # -----------------------------
    overall_mean = np.mean(chain_means)

    # -----------------------------
    # 3. Between-chain variance B
    # -----------------------------
    B = (n / (m - 1)) * np.sum(
        (chain_means - overall_mean) ** 2
    )

    # -----------------------------
    # 4. Within-chain variance W
    # -----------------------------
    chain_variances = np.var(chains, axis=1, ddof=1)

    W = np.mean(chain_variances)

    # -----------------------------
    # 5. Posterior variance estimate
    # -----------------------------
    V_hat = ((n - 1) / n) * W + (1 / n) * B

    # -----------------------------
    # 6. R-hat
    # -----------------------------
    R_hat = np.sqrt(V_hat / W)

    return {
        "B": B,
        "W": W,
        "V_hat": V_hat,
        "R_hat": R_hat
    }