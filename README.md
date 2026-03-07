# Student Management System (AI/ML Showcase)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://student-management-system-dropout-prediction.streamlit.app)

An interview-ready portfolio project for student dropout risk prediction using machine learning, explainability, and a Streamlit demo app.

## Live Demo

Try the deployed app — no setup required:

**https://student-management-system-dropout-prediction.streamlit.app**

## What This Project Demonstrates

- End-to-end ML workflow: data ingestion, feature engineering, training, evaluation
- Multiple model families: Logistic Regression, Random Forest, XGBoost
- Explainability with SHAP (global and per-student insights)
- User-facing interfaces:
  - CLI flow for structured data entry and local CSV persistence
  - Streamlit app for interactive prediction and explanation

## Current Version

`v1.6.0`

Completed milestones:
- `v1.1`: package scaffold and tooling
- `v1.2`: Kaggle dataset integration and EDA
- `v1.3`: baseline and tuned ML models
- `v1.4`: explainability and experiments
- `v1.5`: Streamlit + CLI data workflows
- `v1.6`: interview polish artifacts and test coverage

## Project Structure

```text
student-management-system/
├── student_management/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── core.py
│   ├── data_ingest.py
│   ├── features.py
│   ├── training.py
│   └── evaluate.py
├── data/
│   ├── sample_students.csv
│   ├── feedback_data.csv
│   └── cli_data.csv
├── models/
├── notebooks/
├── results/
│   └── MODEL_METRICS.json
├── scripts/
│   └── run_demo.ps1
└── tests/
    ├── test_smoke.py
    └── test_training.py
```

## Quick Start

### 1. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the CLI app

```powershell
python -m student_management
```

### 4. Run the Streamlit demo

```powershell
streamlit run streamlit_app.py
```

Or use the helper script:

```powershell
.\scripts\run_demo.ps1
```

## Training and Evaluation

Train models:

```powershell
python -m student_management.training
```

Evaluate a saved model directory:

```powershell
python -c "from student_management.evaluate import evaluate_model; evaluate_model('models/logistic_tuned')"
```

## Tests and Quality

Run smoke tests:

```powershell
pytest tests/test_smoke.py -q
```

Run training pipeline tests:

```powershell
pytest tests/test_training.py -q
```

Run formatting/lint hooks:

```powershell
pre-commit run --all-files
```

## Key Artifacts

- Demo walkthrough: `demo.md`
- One-page summary: `PROJECT_SUMMARY.md`
- Artifact inventory and model metrics: `results/MODEL_METRICS.json`

## Author

Yuval Shah  
GitHub: `@yuvalshahtech`  
Live Demo: https://student-management-system-dropout-prediction.streamlit.app
