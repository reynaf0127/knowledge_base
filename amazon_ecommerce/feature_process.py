import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
data = pd.read_csv('./amazon_ecommerce/remove_outliers.csv')
print(data.columns)
data['is_return_number'] = data['is_returned'].astype(int)
unused_list = ['user_id','product_id','seller_id','delivery_status','Unnamed: 0','price','final_price','review_count_log','rating_log','is_return_number']
target = 'is_returned'
x = data.drop(columns=[target]+unused_list)
x_number = x.select_dtypes(include=['number','bool'])
print(x_number.columns)
x_category = x.select_dtypes(include=['object','category'])
y = data[target]
# ----------------------
# feature explore
# ----------------------
numeric_result = []
for col in x_number.columns:
    temp = data.groupby(target)[col].mean().reset_index()
    temp['feature'] = col
    numeric_result.append(temp)
n_col = 3 
n_row = math.ceil(len(x_number.columns) / n_col)
fig, axes = plt.subplots(n_row, n_col, figsize=(5*n_col, 4*n_row))
axes = axes.flatten()
colors = ['#4C78A8', '#F58518']
# target distribution
plt.figure(figsize=(6,6))
data.groupby(target)['is_return_number'].count().plot(kind='pie', autopct='%1.1f%%')
plt.savefig('./amazon_ecommerce/target_distribution.png',bbox_inches='tight')
plt.close()
for i, col in enumerate(x_number.columns):
    temp = data.groupby(target)[col].mean()
    axes[i].bar(temp.index.astype(str),temp.values,color=colors[:len(temp)])
    axes[i].set_title(col, fontsize=12)
    axes[i].set_xlabel(target)
    axes[i].set_ylabel("Mean")
    axes[i].grid(axis='y',alpha=0.3)
plt.tight_layout()
plt.savefig('./amazon_ecommerce/feature_numeric.png',bbox_inches='tight')
plt.close()
category_result = []
for col in x_category.columns:
    temp = data.groupby(col)['is_return_number'].mean().reset_index()
    temp['feature'] = col
    category_result.append(temp)
n_row = math.ceil(len(x_category.columns) / n_col)
fig, axes = plt.subplots(n_row, n_col, figsize=(5*n_col, 4*n_row))
axes = axes.flatten()
for i, col in enumerate(x_category.columns):
    temp = data.groupby(col)['is_return_number'].mean()
    axes[i].bar(temp.index.astype(str),temp.values,color='cornflowerblue')
    axes[i].set_title(col, fontsize=12)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel("Mean")
    axes[i].grid(axis='y',alpha=0.3)
plt.tight_layout()
plt.savefig('./amazon_ecommerce/feature_object.png',bbox_inches='tight')
plt.close()
# ----------------------
# correlation
# ----------------------
corr = x.corr(numeric_only=True)
plt.figure(figsize=(12,10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation between features')
plt.savefig('./amazon_ecommerce/corr_features.png',bbox_inches='tight')
plt.close()
target_data = x.copy()
target_data['is_returned'] = y
corr_target = target_data.corr(numeric_only=True)
corr_target_result = corr_target['is_returned'].sort_values(ascending=False)
print(corr_target_result)
ax = corr_target_result.drop('is_returned').plot(kind='barh',figsize=(8,6),color='darkkhaki')
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f')
plt.title("Correlation with target")
plt.savefig('./amazon_ecommerce/corr_features_target.png',bbox_inches='tight')
plt.close()
# ----------------------
# feature importance
# ----------------------
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(x_number,y)
importance = pd.Series(
    model.feature_importances_,
    index = x_number.columns,
).sort_values(ascending=False)
print(importance)
ax = importance.plot(
    kind = 'barh',
    figsize = (10,6),
    color = 'teal',
)
ax.invert_yaxis()
plt.title('Feature importance (random forest)')
for container in ax.containers:
    ax.bar_label(container,fmt='%.2f')
plt.savefig('./amazon_ecommerce/feature_importance.png',bbox_inches='tight')
plt.close()
# ----------------------
# feature selection
# ----------------------
cumsum = importance.cumsum()
top_features = cumsum[cumsum<= 0.99].index
x_number_top = x_number[top_features]
correlated_features = ['rating','review_count','final_price_log']
x_number_top = x_number_top.drop(columns=correlated_features)
from joblib import dump
dump((x_number_top, y), "./amazon_ecommerce/features.joblib")