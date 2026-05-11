from joblib import load, dump
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

# -------------------
# Load data
# -------------------
X_selected, y = load("./amazon_ecommerce/features.joblib")
print(X_selected.columns)
X_train, X_test, y_train, y_test = train_test_split(
    X_selected,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# -------------------
# Define models
# -------------------
models = {
    "Logistic regression": LogisticRegression(max_iter=1000, class_weight='balanced'),
    "Random forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight='balanced'
    ),
    "Gradient boosting": GradientBoostingClassifier(random_state=42),
    "Decision tree": DecisionTreeClassifier(
        random_state=42,
        class_weight='balanced'
    )
}

# -------------------
# Create output folders
# -------------------
model_dir = Path('./amazon_ecommerce/models')
result_dir = Path('./amazon_ecommerce/results')
model_dir.mkdir(parents=True, exist_ok=True)
result_dir.mkdir(parents=True, exist_ok=True)

# -------------------
# Train and evaluate
# -------------------
results = []
threshold_results = []
thresholds = np.arange(0.1, 0.91, 0.05)
for name, model in models.items():
    print(f'Training {name} ...')
    model.fit(X_train, y_train)
    y_prob = model.predict_proba(X_test)[:,1] # probability of y being 1, y_pred is decision while y_prod is confidence
    best_threshold = 0.5
    best_f1 = -1
    for threshold in thresholds:
        y_pred_threshold = (y_prob >= threshold).astype(int)
        precision = precision_score(y_test, y_pred_threshold, zero_division=0)
        recall = recall_score(y_test, y_pred_threshold, zero_division=0)
        f1 = f1_score(y_test, y_pred_threshold, zero_division=0)
        accuracy = accuracy_score(y_test, y_pred_threshold)
        threshold_results.append({
            "model": name,
            "threshold": threshold,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        })
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    y_pred = (y_prob >= best_threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    result = {
        "model": name,
        "best_threshold": best_threshold,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_prob), # how well the model separate the classes
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "true_positive": tp
    }
    results.append(result)
    safe_name = name.lower().replace(" ","_")
    dump(model, model_dir / f'{safe_name}.joblib')

# -------------------
# Save result table
# -------------------
result_df = pd.DataFrame(results)
result_df = result_df.sort_values('roc_auc',ascending=False)
result_df.to_csv(result_dir / 'model_comparison.csv', index=False)