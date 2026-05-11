from joblib import load,dump
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import statsmodels.api as sm

X, y = load('./MMM/data/mmm_features.joblib')
X = X.replace([np.inf,-np.inf], np.nan)
X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

models = {
    "OLS": LinearRegression(positive=True), # ordianry least square, fine coef to minimize the square error, linear regression (unstable coef, can't handle multicollinearity), good for baseline and understand effect not good for final model
    "Ridge": Ridge(alpha=1.0,positive=True), # OLS + penalty large coef: minimize error + alpha * (sum of squared coef) (stable coef, handle multicollinearity)
    "Lasso": Lasso(alpha=0.01,positive=True), # OLS + force some coef to 0: minimize error + alpha * (sum of absolute coef) (remove weak features, works as feature selection, unstable)
    "ElasticNet": ElasticNet(alpha=0.01, l1_ratio=0.5,positive=True), # combine ridge and lasso, (alpha is regularization, 0.0001 almost OLS, 0.01 mild penalty, 1.0 strong, 10 bery strong, model too simple and underfit) (l1_ratio: 0 pure Ridge, 1 pure Lasso)
    "XGboost": XGBRegressor(n_estimators=200) # tree based, learn non linear relation (hard to interpret bu powerful for prediction) number of trees = 200 moderate complexity
}
results = []
trained_model = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    results.append({
        "model": name,
        "R2_train": r2_score(y_train, y_train_pred),
        "mae_train": mean_absolute_error(y_train, y_train_pred),
        "R2_test": r2_score(y_test, y_test_pred),
        "mae_test": mean_absolute_error(y_test, y_test_pred)
    })
    trained_model[name] = model

results_df = pd.DataFrame(results)
results_df.to_csv('./MMM/model_comparison.csv')
# -------------
# best model
# -------------
result_df_filtered = results_df[
    results_df["model"].isin(["OLS", "Ridge", "Lasso", "ElasticNet"])
]
best_model_name = result_df_filtered.sort_values(by=['R2_test','mae_test'],ascending=[False,True]).iloc[0]['model']
best_model = trained_model[best_model_name]
output_dir = Path('./MMM/output')
output_dir.mkdir(parents=True,exist_ok=True)
dump(best_model, output_dir/'mmm_model.joblib')
coef_df = pd.DataFrame({
    'features': X.columns,
    'coef': best_model.coef_
})
coef_df = coef_df.sort_values('coef',ascending=False)
coef_df.to_csv(output_dir/'mmm_coef.csv', index=False)
# -------------
# total prediction
# -------------
contribution_df = pd.DataFrame(index=X.index)
for feature, coef in zip(X.columns, best_model.coef_):
    contribution_df[feature] = X[feature] * coef
contribution_df['base'] = best_model.intercept_
contribution_df['predicted_total'] = contribution_df.sum(axis=1)
contribution_df['actual'] = y
contribution_df.to_csv(output_dir/'mmm_contribution.csv', index=False)
# -------------
# channel contribution
# -------------
media_cols = [
    "tv", "digital", "sponsorship", "content_marketing",
    "online_marketing", "affiliates", "sem", "radio", "other"
]
media_feature_cols = []
for col in media_cols:
    possible_names = [col+'_sat']
    for name in possible_names:
        if name in X.columns:
            media_feature_cols.append(name)
channel_contribution = (
    contribution_df[media_feature_cols]
    .sum()
    .reset_index()
)
channel_contribution.columns = ['channel_feature','contribution']
channel_contribution['channel'] = (
    channel_contribution['channel_feature']
    .str.replace('_sat',"",regex=False)
)
channel_contribution = channel_contribution.sort_values('contribution',ascending=False)
channel_contribution.to_csv(output_dir/'channel_contribution.csv',index=False)
# -------------
# roi
# -------------
df = pd.read_csv('./MMM/data/merge_df.csv')
roi_rows = []
for channel in media_cols:
    spend = df[channel].sum()
    contribution_match = channel_contribution[channel_contribution['channel']==channel]
    if contribution_match.empty:
        contribution = 0
    else: 
        contribution = contribution_match['contribution'].sum()
    roi = contribution / spend if spend!=0 else np.nan
    roi_rows.append({
        'channel':channel,
        'spend':spend,
        'contribution':contribution,
        'roi':roi
    })
roi_df =pd.DataFrame(roi_rows)
roi_df = roi_df.sort_values('roi',ascending=False)
roi_df.to_csv(output_dir/'channel_roi.csv',index=False)