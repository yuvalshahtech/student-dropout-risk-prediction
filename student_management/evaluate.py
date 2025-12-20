import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from student_management.features import build_features

def evaluate_model(data_path, model_path):
    X, y, _ = build_features(data_path)
    pipeline = joblib.load(model_path)
    y_pred = pipeline.predict(X)

    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average="weighted")
    recall = recall_score(y, y_pred, average="weighted")
    f1 = f1_score(y, y_pred, average="weighted")

    y_proba = pipeline.predict_proba(X)
    roc_auc = roc_auc_score(y, y_proba, multi_class="ovr", average="weighted")

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("ROC-AUC:",roc_auc)

    y_bin = label_binarize(y, classes=pipeline.classes_)

    plt.figure()
    for i, cls in enumerate(pipeline.classes_):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_proba[:, i])
        plt.plot(fpr, tpr, label=f"ROC for class {cls}")
    plt.plot([0,1], [0,1], linestyle="--", color="grey")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.show()

    return {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "roc_auc": roc_auc
}
