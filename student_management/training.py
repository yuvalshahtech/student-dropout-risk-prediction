from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from student_management.features import build_features
import os

def train_model(data_path, model_type="logistic", out_dir="models"):
    X, y, preprocessor = build_features(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    if model_type == "logistic":
        model = LogisticRegression(max_iter=1000)
    elif model_type == "rf":
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
    else:
        raise ValueError("Unsupported model type")
    
    pipeline = Pipeline([
        ("preprocessing", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    os.makedirs(out_dir, exist_ok=True)

    model_path = f"{out_dir}/model.joblib"
    joblib.dump(pipeline, model_path)

    print(f"Model saved to {model_path}")
