import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import ast

def build_features(data_path):
    data = pd.read_csv(data_path)
    data["avg_assignment_score"] = data["assignment_scores"].apply(
        lambda x: sum(ast.literal_eval(x)) / len(ast.literal_eval(x))
    )
    X = data.drop(
        columns=["final_grade", "student_id", "assignment_scores"]
    )
    y = data["final_grade"]

    numerical_features = ["age", "attendance_pct", "avg_assignment_score"]
    categorical_features = ["gender", "course_history"]

    num_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(sparse_output=False, handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_pipeline, numerical_features),
        ("cat", cat_pipeline, categorical_features)
    ])

    return X, y, preprocessor