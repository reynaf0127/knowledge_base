import matplotlib.pyplot as plt
from joblib import load
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

model = load('./MMM/output/mmm_model.joblib')
X, y = load('./MMM/data/mmm_features.joblib')
X = X.replace([np.inf,-np.inf], np.nan)
X = X.fillna(0)
# -------------
# actual vs predict
# -------------
y_pred = model.predict(X)
residuals = y - y_pred
plt.figure(figsize=(10,6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(),y.max()],[y.min(),y.max()],'r--')
plt.xlabel('Acutal GMV')
plt.ylabel('Predict GMV')
plt.show()
# -------------
# residual plot
# -------------
plt.figure(figsize=(10,6))
plt.scatter(y_pred,residuals,alpha=0.6)
plt.axhline(0, color='red',linestyle='--')
plt.xlabel('Predict GMV')
plt.ylabel('Residual')
plt.show()
# -------------
# channel contribution
# -------------
channel_contribute = pd.read_csv('./MMM/output/channel_contribution.csv')
plt.figure(figsize=(10,6))
plt.bar(channel_contribute['channel'],channel_contribute['contribution'],color='coral')
plt.xticks(rotation=45)
plt.show()
# -------------
# channel roi
# -------------
channel_roi = pd.read_csv('./MMM/output/channel_roi.csv')
plt.figure(figsize=(10,6))
plt.bar(channel_roi['channel'],channel_roi['roi'],color='olive')
plt.xticks(rotation=45)
plt.show()
# -------------
# daily contribution
# -------------
media_cols = [
    "tv", "digital", "sponsorship", "content_marketing",
    "online_marketing", "affiliates", "sem", "radio", "other"
]
mmm_contribution = pd.read_csv('./MMM/output/mmm_contribution.csv')
plt.figure(figsize=(10,6))
for col in media_cols:
    new_col = col + '_sat'
    plt.plot(mmm_contribution.index,mmm_contribution[new_col],label=col)
plt.legend()
plt.title('Daily media contribution')
plt.show()