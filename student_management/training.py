from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
import joblib
from student_management.features import build_features
import os
from xgboost import XGBClassifier


def train_model(data_path, model_type="logistic", out_dir="models", tune=False):
    X, y, preprocessor = build_features(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    if model_type == "logistic":
        model = LogisticRegression(max_iter=2000)
        if tune:
            param_grid = {
                "model__C": [0.01, 0.1, 1, 10],
                "model__penalty": ["l2"],
                "model__class_weight": ["balanced", None]
            }
            model = GridSearchCV(
                estimator=Pipeline([
                    ("preprocessing", preprocessor),
                    ("model", LogisticRegression(max_iter=2000))
                ]),
                param_grid=param_grid,
                cv=5,
                scoring="roc_auc",
                n_jobs=-1
            )
            model.fit(X_train, y_train)
            best_pipeline = model.best_estimator_
        else:
            best_pipeline = Pipeline([
                ("preprocessing", preprocessor),
                ("model", model)
            ])
            best_pipeline.fit(X_train, y_train)
    elif model_type == "rf":
        base_rf = RandomForestClassifier(random_state=42)
        if tune:
            param_grid = {
                "model__n_estimators": [200, 400],
                "model__max_depth": [None, 10, 20],
                "model__min_samples_split": [2, 5],
                "model__class_weight": ["balanced"]
            }
            model = GridSearchCV(
                estimator=Pipeline([
                    ("preprocessing", preprocessor),
                    ("model", base_rf)
                ]),
                param_grid=param_grid,
                cv=5,
                scoring="roc_auc",
                n_jobs=-1
            )
            model.fit(X_train, y_train)
            best_pipeline = model.best_estimator_
        else:
            best_pipeline = Pipeline([
                ("preprocessing", preprocessor),
                ("model", base_rf)
            ])
            best_pipeline.fit(X_train, y_train)
    elif model_type == "xgb":
        base_xgb = XGBClassifier(
            eval_metric="auc",
            random_state=42
        )
        if tune:
            param_dist = {
                "model__n_estimators": [500, 800],
                "model__max_depth": [6, 8, 10],
                "model__learning_rate": [0.01, 0.03],
                "model__subsample": [0.8, 1.0],
                "model__colsample_bytree": [0.8, 1.0]
            }
            model = RandomizedSearchCV(
                estimator=Pipeline([
                    ("preprocessing", preprocessor),
                    ("model", base_xgb)
                ]),
                param_distributions=param_dist,
                n_iter=15,
                cv=5,
                scoring="roc_auc",
                n_jobs=-1,
                random_state=42
            )
            model.fit(X_train, y_train)
            best_pipeline = model.best_estimator_
        else:
            best_pipeline = Pipeline([
                ("preprocessing", preprocessor),
                ("model", base_xgb)
            ])

            best_pipeline.fit(X_train, y_train)
    else:
        raise ValueError("Unsupported model type")
    os.makedirs(out_dir, exist_ok=True)
    model_path = f"{out_dir}/model.joblib"
    joblib.dump(best_pipeline, model_path)
    test_path = f"{out_dir}/test_data.joblib"
    joblib.dump((X_test, y_test), test_path)
    print("Model saved to:", model_path)
    print("Test data saved to:", test_path)
    return best_pipeline