import pandas as pd
import numpy as np
from joblib import load

from meridian.data.data_frame_input_data_builder import DataFrameInputDataBuilder
from meridian.model.model import Meridian
from meridian.model import spec as specmod
from meridian.analysis import visualizer, summarizer, optimizer


# -----------------------------
# 1. Load your MMM dataset
# -----------------------------
data = pd.read_csv('./MMM/data/merge_df.csv')
df = data["df"].copy()

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[ &\-]+", "_", regex=True)
    .str.replace(r"_+", "_", regex=True)
)

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
kpi_col = "total_gmv"

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
    "independence_sale",
    "republic_day",
    "valentine_s_day"
]

media_cols = [c for c in media_cols if c in df.columns]
control_cols = [c for c in control_cols if c in df.columns]

df = df[["date", kpi_col] + media_cols + control_cols].copy()
df = df.replace([np.inf, -np.inf], np.nan).fillna(0)


# -----------------------------
# 3. Add geo column if national-level data
# Meridian can handle geo-level data, but national-level can use one geo.
# -----------------------------
df["geo"] = "national"


# -----------------------------
# 4. Build Meridian input data
# -----------------------------
builder = DataFrameInputDataBuilder(
    kpi_type="revenue",
    default_kpi_column=kpi_col,
    default_time_column="date",
    default_geo_column="geo",
)

builder = builder.with_media(
    media_cols=media_cols,
    media_spend_cols=media_cols,
)

if control_cols:
    builder = builder.with_controls(control_cols=control_cols)

input_data = builder.build(df)


# -----------------------------
# 5. Configure and fit Meridian model
# -----------------------------
model_spec = specmod.ModelSpec()

mmm = Meridian(
    input_data=input_data,
    model_spec=model_spec,
)
# bayesian sampleing
mmm.sample_posterior(
    n_chains=4,
    n_adapt=1000,
    n_burnin=500,
    n_keep=1000,
    seed=42,
)


# -----------------------------
# 6. Diagnostics / results
# -----------------------------
model_diagnostics = visualizer.ModelDiagnostics(mmm)
model_diagnostics.plot_rhat_boxplot()

model_fit = visualizer.ModelFit(mmm)
model_fit.plot_model_fit()

summary = summarizer.Summarizer(mmm)
summary.output_model_results_summary("./MMM/output/meridian_model_summary.html")


# -----------------------------
# 7. Budget optimization
# -----------------------------
budget_optimizer = optimizer.BudgetOptimizer(mmm)

optimization_results = budget_optimizer.optimize()

print(optimization_results)