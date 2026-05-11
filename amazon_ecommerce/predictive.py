from joblib import load
import pandas as pd
import numpy as np
comparison = pd.read_csv('./amazon_ecommerce/results/model_comparison.csv')
best_model = comparison.sort_values('roc_auc',ascending=False).iloc[0]['model']
safe_name = best_model.lower().replace(" ","_")
model = load(f'./amazon_ecommerce/models/{safe_name}.joblib')
model_features = model.feature_names_in_
X, y = load('./amazon_ecommerce/features.joblib')
preprocess = load('./amazon_ecommerce/preprocess.joblib')
print('feature names:', list(X.columns))

def transform_input(input_data):
    scaler = preprocess['scaler']
    num_cols = preprocess['num_cols']
    lower_review = preprocess['lower_review']
    upper_review = preprocess['upper_review']
    lower_rating = preprocess['lower_rating']
    upper_rating = preprocess['upper_rating']
    if isinstance(input_data, dict):
        input_df = pd.DataFrame([input_data])
    else:
        input_df = input_data.copy()
    # log transform
    input_df['price_log'] = np.log1p(input_df['price'])
    input_df['final_price_log'] = np.log1p(input_df['final_price'])
    input_df['review_count_log'] = np.log1p(input_df['review_count'])
    input_df['rating_log'] = np.log1p(input_df['rating'])
    # capping winsorization
    input_df['review_count_log_capped'] = np.clip(
        input_df['review_count_log'], 
        lower_review, 
        upper_review
    )
    input_df['rating_log_capped'] = np.clip(
        input_df['rating_log'], 
        lower_rating,
        upper_rating
    )
    # make sure all scaler columns exist
    missing_scale_cols = [col for col in num_cols if col not in input_df.columns]
    if missing_scale_cols:
        raise ValueError(f"Missing columns needed for scaler: {missing_scale_cols}")
    # standardize numeric columns in same order as training
    input_df[num_cols] = scaler.transform(input_df[num_cols])
    # remove features you do not want to use in model
    drop_after_scaling = [
        'final_price',
        'final_price_log',
        'shipping_time_days'
    ]
    input_df = input_df.drop(columns=drop_after_scaling, errors='ignore')
    return input_df

def predict_return_risk(input_data):
    feature_name = list(model_features)
    input_df = transform_input(input_data)
    x_input = input_df[feature_name]
    missing_features = [col for col in feature_name if col not in input_df.columns]
    if missing_features:
        raise ValueError(f"Missing required features for prediction: {missing_features}")
    return_prob = model.predict_proba(x_input)[:,1]
    prediction = (return_prob >= 0.5).astype(int)
    result = input_df.copy()
    result['return_probability'] = return_prob
    result['return_risk_percent'] = (return_prob * 100).round(2)
    result['predicted_return'] = prediction
    return result