import pandas as pd
import numpy as np
from joblib import dump

df = pd.read_csv('./MMM/data/merge_df.csv')
upper = df['total_gmv_'].quantile(0.99)
df['total_gmv_'] = np.clip(df['total_gmv_'], None, upper)
df['log_gmv'] = np.log1p(df['total_gmv_'])
df = df.rename(columns={
    "Date_": "date",
    "total_gmv_": "total_gmv",
    "total_units_": "total_units",
    "total_mrp_": "total_mrp",
    "total_discount_": "total_discount"
})
drop_cols = [
    "date_x", "date_y", "date_daily",
    "days_in_month", "day_number"
]
df = df.drop(columns=drop_cols, errors="ignore")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
media_cols = [
    "tv", "digital", "sponsorship", "content_marketing",
    "online_marketing", "affiliates", "sem", "radio", "other"
]
control_cols = [
    "total_discount",
    "bed", "bsd-5", "big_diwali_sale",
    "christmas___new_year_sale", "daussera_sale",
    "eid___rathayatra_sale", "independence_sale",
    "republic_day", "valentine_s_day"
]
# -------------
# adstock: how advertising impact carries over time, Advertising today still affects sales tomorrow (and days after)
# -------------
def adstock(series, decay):
    result = []
    prev = 0
    for x in series:
        val = x + decay * prev
        result.append(val)
        prev = val
    return pd.Series(result, index=series.index)
decay_map = {
    "tv": 0.8,
    "digital": 0.5,
    "sponsorship": 0.7,
    "sem": 0.2,
    "radio": 0.6
}
for col in media_cols:
    decay = decay_map.get(col,0.5)
    df[col + "_adstock"] = adstock(df[col], decay)
# -------------
# Saturation diminishing return
# -------------
def saturation(x, alpha=0.001):
    return 1-np.exp(-alpha * x)
for col in media_cols:
    df[col + '_sat'] = saturation(df[col + '_adstock'])
# -------------
# prepare modeling dataset
# -------------
feature_cols = [col + '_sat' for col in media_cols] + control_cols
X = df[feature_cols]
y = df['log_gmv']
dump((X,y), './MMM/data/mmm_features.joblib')