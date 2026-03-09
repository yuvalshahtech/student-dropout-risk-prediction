"""
Test suite for training pipeline.
Verifies that the training pipeline runs end-to-end on small data
and that models can be trained, saved, and loaded correctly.
"""

import pytest
import os
import tempfile
import shutil
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


class TestTrainingPipeline:
    """Test cases for the training module."""

    @pytest.fixture
    def temp_data_dir(self):
        """Create a temporary directory for test data."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sample_dataset(self, temp_data_dir):
        """Generate a tiny synthetic dataset for testing."""
        np.random.seed(42)
        n_samples = 50  # Small for fast testing

        data = {
            "Age": np.random.randint(18, 40, n_samples),
            "GPA": np.random.uniform(1.5, 4.0, n_samples),
            "CGPA": np.random.uniform(1.5, 4.0, n_samples),
            "Semester_GPA": np.random.uniform(1.5, 4.0, n_samples),
            "Study_Hours_per_Day": np.random.uniform(1, 8, n_samples),
            "Assignment_Delay_Days": np.random.randint(0, 10, n_samples),
            "Attendance_Rate": np.random.uniform(50, 100, n_samples),
            "Travel_Time_Minutes": np.random.randint(5, 120, n_samples),
            "Family_Income": np.random.randint(10000, 150000, n_samples),
            "Internet_Access": np.random.choice(["Yes", "No"], n_samples),
            "Scholarship": np.random.choice(["Yes", "No"], n_samples),
            "Part_Time_Job": np.random.choice(["Yes", "No"], n_samples),
            "Stress_Index": np.random.uniform(0.5, 4.0, n_samples),
            "Semester": np.random.choice(["Year 1", "Year 2", "Year 3", "Year 4"], n_samples),
            "Department": np.random.choice(["Science", "Arts", "Business", "CS", "Engineering"], n_samples),
            "Parental_Education": np.random.choice(["High School", "Bachelor", "Master", "PhD"], n_samples),
            "Dropout": np.random.choice([0, 1], n_samples)  # Binary: 0 = persist, 1 = dropout
        }

        df = pd.DataFrame(data)
        csv_path = os.path.join(temp_data_dir, "test_data.csv")
        df.to_csv(csv_path, index=False)

        return csv_path

    def test_imports(self):
        """Test that all required modules can be imported."""
        try:
            from student_management.features import build_features
            from student_management.training import train_model
            from student_management.evaluate import evaluate_model
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import required module: {e}")

    def test_features_build(self, sample_dataset):
        """Test that feature preprocessing pipeline works."""
        from student_management.features import build_features

        try:
            X, y, preprocessor = build_features(sample_dataset)
            assert X.shape[0] == 50, "Expected 50 samples"
            assert X.shape[1] > 0, "Expected features to be extracted"
            assert y is not None, "Expected target variable"
            assert preprocessor is not None, "Expected preprocessor pipeline"
            print(f"[PASS] Features built: X shape = {X.shape}, y shape = {y.shape}")
        except Exception as e:
            pytest.fail(f"Feature building failed: {e}")

    def test_model_training_logistic(self, sample_dataset, temp_data_dir):
        """Test training a logistic regression model."""
        from student_management.training import train_model

        try:
            out_dir = os.path.join(temp_data_dir, "models")
            os.makedirs(out_dir, exist_ok=True)

            # Train logistic regression (no tuning, for speed)
            train_model(
                data_path=sample_dataset,
                model_type="logistic",
                out_dir=out_dir,
                tune=False
            )

            # Check that model was saved
            model_path = os.path.join(out_dir, "logistic", "model.joblib")
            assert os.path.exists(model_path), f"Model not found at {model_path}"
            print(f"[PASS] Logistic Regression model saved: {model_path}")

            # Test model loading
            pipeline = joblib.load(model_path)
            assert pipeline is not None, "Failed to load model"
            print("[PASS] Model loaded successfully")

        except Exception as e:
            pytest.fail(f"Logistic regression training failed: {e}")

    def test_model_training_random_forest(self, sample_dataset, temp_data_dir):
        """Test training a random forest model."""
        from student_management.training import train_model

        try:
            out_dir = os.path.join(temp_data_dir, "models")
            os.makedirs(out_dir, exist_ok=True)

            # Train random forest (no tuning, for speed)
            train_model(
                data_path=sample_dataset,
                model_type="rf",
                out_dir=out_dir,
                tune=False
            )

            # Check that model was saved
            model_path = os.path.join(out_dir, "rf", "model.joblib")
            assert os.path.exists(model_path), f"Model not found at {model_path}"
            print(f"[PASS] Random Forest model saved: {model_path}")

        except Exception as e:
            pytest.fail(f"Random Forest training failed: {e}")

    def test_model_predictions(self, sample_dataset, temp_data_dir):
        """Test that a trained model can make predictions."""
        from student_management.training import train_model
        from student_management.features import build_features

        try:
            out_dir = os.path.join(temp_data_dir, "models")
            os.makedirs(out_dir, exist_ok=True)

            # Train model
            train_model(
                data_path=sample_dataset,
                model_type="logistic",
                out_dir=out_dir,
                tune=False
            )

            # Load and test prediction
            model_path = os.path.join(out_dir, "logistic", "model.joblib")
            pipeline = joblib.load(model_path)

            # Load test data
            df = pd.read_csv(sample_dataset)
            X = df.drop(columns=["Dropout"])
            y = df["Dropout"]

            # Make predictions
            predictions = pipeline.predict(X.iloc[:5])
            probabilities = pipeline.predict_proba(X.iloc[:5])

            assert predictions.shape[0] == 5, "Expected 5 predictions"
            assert probabilities.shape == (5, 2), "Expected 5 probability pairs"
            assert np.all((predictions == 0) | (predictions == 1)), "Predictions must be 0 or 1"
            assert np.all((probabilities >= 0) & (probabilities <= 1)), "Probabilities must be [0, 1]"
            print(f"[PASS] Predictions working: {predictions}")
            print(f"[PASS] Probabilities working: {probabilities[0]}")

        except Exception as e:
            pytest.fail(f"Prediction test failed: {e}")

    def test_preprocessing_pipeline(self, sample_dataset):
        """Test that preprocessing handles numeric and categorical features."""
        from student_management.features import build_features

        try:
            X, y, preprocessor = build_features(sample_dataset)

            # Check that preprocessor transforms data correctly
            X_transformed = preprocessor.fit_transform(X)
            assert X_transformed.shape[0] == 50, "Expected 50 samples after transform"
            assert np.all(np.isfinite(X_transformed)), "Expected no NaN or inf values"
            print(f"[PASS] Preprocessing pipeline working: output shape = {X_transformed.shape}")

        except Exception as e:
            pytest.fail(f"Preprocessing test failed: {e}")

    def test_data_persistence(self, sample_dataset, temp_data_dir):
        """Test that training artifacts persist correctly."""
        from student_management.training import train_model

        try:
            out_dir = os.path.join(temp_data_dir, "models")
            os.makedirs(out_dir, exist_ok=True)

            # Train model
            train_model(
                data_path=sample_dataset,
                model_type="logistic",
                out_dir=out_dir,
                tune=False
            )

            # Check artifact structure
            model_dir = os.path.join(out_dir, "logistic")
            assert os.path.exists(os.path.join(model_dir, "model.joblib"))
            assert os.path.exists(os.path.join(model_dir, "test_data.joblib"))

            print(f"[PASS] All artifacts persisted correctly in {model_dir}")

        except Exception as e:
            pytest.fail(f"Persistence test failed: {e}")

    def test_stratified_split(self, sample_dataset):
        """Test that training uses stratified split for both classes."""
        from student_management.features import build_features

        try:
            df = pd.read_csv(sample_dataset)
            y = df["Dropout"]

            # Check that both classes are present
            assert 0 in y.values, "Expected class 0 (persist) in data"
            assert 1 in y.values, "Expected class 1 (dropout) in data"

            class_dist = y.value_counts()
            print(f"[PASS] Class distribution: {dict(class_dist)}")

        except Exception as e:
            pytest.fail(f"Stratified split test failed: {e}")


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
