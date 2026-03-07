from student_management.features import build_features
import shap
import joblib


def explain_single_student(model_path: str, data_path: str, student_index: int):
    # Load pipeline
    pipeline = joblib.load(model_path)

    preprocessor = pipeline.named_steps["preprocessing"]
    model = pipeline.named_steps["model"]

    # Use SAME feature builder as training
    X, y, _ = build_features(data_path)

    # Transform using trained preprocessor
    X_processed = preprocessor.transform(X)

    feature_names = preprocessor.get_feature_names_out()

    model_name = type(model).__name__
    if model_name in ["RandomForestClassifier", "XGBClassifier"]:
        explainer = shap.TreeExplainer(model)
    elif model_name == "LogisticRegression":
        explainer = shap.LinearExplainer(model, X_processed)
    else:
        raise ValueError("Model not supported for SHAP explanation")
    shap_values = explainer.shap_values(X_processed)

    prediction = model.predict(X_processed[student_index:student_index+1])[0]
    class_index = list(model.classes_).index(prediction)

    # Handle both SHAP formats safely
    if isinstance(shap_values, list):
        student_shap = shap_values[class_index][student_index]
        expected_value = explainer.expected_value[class_index]

    elif hasattr(shap_values, "ndim") and shap_values.ndim == 2:
        student_shap = shap_values[student_index]
        expected_value = explainer.expected_value

    else:
        student_shap = shap_values[student_index, :, class_index]
        expected_value = explainer.expected_value[class_index]

    return {
        "prediction": prediction,
        "expected_value": expected_value,
        "shap_values": student_shap,
        "feature_names": feature_names,
        "processed_features": X_processed[student_index]
    }

def explain_global_model(model_path, data_path):
    import joblib
    import shap
    from student_management.features import build_features

    # Load data
    X, y, _ = build_features(data_path)

    # Load pipeline
    pipeline = joblib.load(model_path)

    model = pipeline.named_steps["model"]
    preprocessor = pipeline.named_steps["preprocessing"]

    # Transform features
    X_processed = preprocessor.transform(X)
    feature_names = preprocessor.get_feature_names_out()

    # Create SHAP explainer
    model_name = type(model).__name__
    if model_name in ["RandomForestClassifier", "XGBClassifier"]:
        explainer = shap.TreeExplainer(model)
    elif model_name == "LogisticRegression":
        explainer = shap.LinearExplainer(model, X_processed)
    else:
        raise ValueError("Model not supported for SHAP explanation")
    shap_values = explainer.shap_values(X_processed)

    return {
        "explainer": explainer,
        "shap_values": shap_values,
        "processed_features": X_processed,
        "feature_names": feature_names,
        "classes": model.classes_
    }
    
def explain_user_input(model_path, data_path, user_input_df):
    from student_management.features import build_features
    import joblib
    import shap
    import pandas as pd

    pipeline = joblib.load(model_path)
    preprocessor = pipeline.named_steps["preprocessing"]
    model = pipeline.named_steps["model"]

    # Build original dataset features
    X, y, _ = build_features(data_path)

    # Append user input (in memory only)
    X = pd.concat([X, user_input_df], ignore_index=True)

    # Transform
    X_processed = preprocessor.transform(X)
    feature_names = preprocessor.get_feature_names_out()
    model_name = type(model).__name__
    if model_name in ["RandomForestClassifier", "XGBClassifier"]:
        explainer = shap.TreeExplainer(model)
    elif model_name == "LogisticRegression":
        explainer = shap.LinearExplainer(model, X_processed)
    else:
        raise ValueError("Model not supported")
    shap_values = explainer.shap_values(X_processed)
    student_index = len(X_processed) - 1
    prediction = model.predict(X_processed[student_index:student_index+1])[0]
    class_index = list(model.classes_).index(prediction)
    if isinstance(shap_values, list):
        student_shap = shap_values[class_index][student_index]
        expected_value = explainer.expected_value[class_index]
    elif hasattr(shap_values, "ndim") and shap_values.ndim == 2:
        student_shap = shap_values[student_index]
        expected_value = explainer.expected_value
    else:
        student_shap = shap_values[student_index, :, class_index]
        expected_value = explainer.expected_value[class_index]
    return {
        "prediction": prediction,
        "expected_value": expected_value,
        "shap_values": student_shap,
        "feature_names": feature_names,
        "processed_features": X_processed[student_index]
    }