import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import dump

df = pd.read_csv('./amazon_ecommerce/amazon_ecommerce_1M.csv')
# -------------------
# Feature engineering
# -------------------
# process outliers
# price, final_price, review_count, rating, 
# log transform for skewed data: price, final_price, review_count
df['price_log'] = np.log1p(df['price'])
df['final_price_log'] = np.log1p(df['final_price'])
df['review_count_log'] = np.log1p(df['review_count'])
df['rating_log'] = np.log1p(df['rating'])
# -------------------
# Winsorization
# -------------------
# capping winsorization for review_count_log, and rating
lower_review = df['review_count_log'].quantile(0.01)
upper_review = df['review_count_log'].quantile(0.99)
df['review_count_log_capped'] = np.clip(df['review_count_log'], lower_review, upper_review)
lower_rating = df['rating_log'].quantile(0.01)
upper_rating = df['rating_log'].quantile(0.99)
df['rating_log_capped'] = np.clip(df['rating_log'], lower_rating, upper_rating)
# -------------------
# Categorical encoding
# -------------------
cats_cols = df.select_dtypes(include=['object','category']).columns.tolist()
exclude_cols = ['user_id','product_id','seller_id','delivery_status']
cats_cols = [col for col in cats_cols if col not in exclude_cols]
cats_cols = [col for col in cats_cols if df[col].nunique() <= 20]
df_encoded = pd.get_dummies(df, columns=cats_cols, drop_first=True)
# -------------------
# Scaling numeric columns
# -------------------
num_cols = df_encoded.select_dtypes(include='number').columns
num_cols = [col for col in num_cols if df[col].dtype != 'bool']
scaler = StandardScaler()
df_scaled = df_encoded.copy()
df_scaled[num_cols] = scaler.fit_transform(df_encoded[num_cols])
# -------------------
# Outlier analysis
# -------------------
# box plot for numeric columns
plt.figure(figsize=(12,6))
sns.boxplot(data=df_scaled[num_cols])
plt.show()
# z score outliers
outlier_count = {}
for col in num_cols:
    z_scores = np.abs(df_scaled[col])
    outliers = z_scores > 3
    outlier_count[col] = outliers.sum()
outlier_df = pd.DataFrame.from_dict(outlier_count,orient='index',columns=['outlier_count'])
outlier_df['outlier_percentage'] = outlier_df['outlier_count'] / len(df) * 100
print(outlier_df.sort_values(by='outlier_percentage',ascending=False))
df_scaled.to_csv('./amazon_ecommerce/remove_outliers.csv')
# save preprocessing objects for future use
preprocess_objects = {
    "scaler": scaler,
    "num_cols": num_cols,
    "cat_cols": cats_cols,
    "lower_review": lower_review,
    "upper_review": upper_review,
    "lower_rating": lower_rating,
    "upper_rating": upper_rating
}
dump(preprocess_objects, "./amazon_ecommerce/preprocess.joblib")