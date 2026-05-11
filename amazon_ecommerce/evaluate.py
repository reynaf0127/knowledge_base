import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
from sklearn.model_selection import train_test_split
# -------------------
# Explore best model
# -------------------
comparison = pd.read_csv('./amazon_ecommerce/results/model_comparison.csv')
best_model = comparison.sort_values('roc_auc',ascending=False).iloc[0]['model']
print("Best model: ", best_model)
ax = comparison.plot(
    x='model',
    y='roc_auc',
    kind='barh',
    figsize=(8,6),
    color='darkkhaki',
    legend=False
)
ax.set_title='Model ROC-AUC Comparison'
for container in ax.containers:
    ax.bar_label(container,fmt='%.2f')
plt.savefig("./amazon_ecommerce/results/model_comparison_auc.png", dpi=300, bbox_inches="tight")
plt.close()

# -------------------
# Evaluate
# -------------------
X_selected, y = load("./amazon_ecommerce/features.joblib")
X_train, X_test, y_train, y_test = train_test_split(
    X_selected,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
safe_name = best_model.lower().replace(" ","_")
model = load(f"./amazon_ecommerce/models/{safe_name}.joblib")
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
plt.title('Confusion matrix')
plt.savefig("./amazon_ecommerce/results/confusion_matrix.png", dpi=300, bbox_inches="tight")
plt.close()
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title("ROC curve")
plt.savefig("./amazon_ecommerce/results/roc_curve.png", dpi=300, bbox_inches="tight")
plt.close()