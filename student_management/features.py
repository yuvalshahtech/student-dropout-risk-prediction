import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import numpy as np


def build_features(data_path):
    data = pd.read_csv(data_path)
    binary_cols = ["Internet_Access", "Scholarship", "Part_Time_Job"]
    for col in binary_cols:
        data[col] = data[col].map({"Yes":1, "No":0})
    data["Parental_Education"] = data["Parental_Education"].fillna("Unknown")

    #Feature Engineering
    data["Dept_Semester"] = data["Department"] + "_" + data["Semester"]
    data["Income_Stress_Ratio"] = data["Stress_Index"] / (data["Family_Income"] + 1)
    data["GPA_vs_CGPA"] = data["GPA"] - data["CGPA"]
    data["GPA_vs_SGPA"] = data["GPA"] - data["Semester_GPA"]
    data["Job_Stress_Interaction"] = data["Part_Time_Job"] * data["Stress_Index"]
    data["Student_Pressure_Index"] = (data["Assignment_Delay_Days"] + data["Travel_Time_Minutes"] +
    data["Part_Time_Job"] + data["Stress_Index"]) / (data["Attendance_Rate"] + data["Study_Hours_per_Day"] + 0.01)
    data["Academic_Risk"] = ((data["Attendance_Rate"] < 75).astype(int) + (data["Study_Hours_per_Day"] < 2).astype(int) + (data["Assignment_Delay_Days"] > 5).astype(int))
    
    X = data.drop(
        columns=["Student_ID", "Gender", "Dropout", "Department", "Semester", "Family_Income","GPA"]
    )

    y = data["Dropout"]

    categorical_features = ["Parental_Education", "Dept_Semester"]
    numerical_features = X.drop(columns=categorical_features).columns.tolist()
    
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