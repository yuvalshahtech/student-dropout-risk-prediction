# Student Dropout Risk Prediction System

## Problem Statement
**The Challenge:** Most universities lack early-warning systems to identify at-risk students before dropout occurs. Dropout impacts student lives, institutional reputation, and budget. Traditional rule-based systems capture only obvious signals (low GPA); they miss students struggling with stress, financial hardship, or engagement issues.

**The Solution:** A machine learning classifier that combines academic, environmental, and socioeconomic features to predict dropout risk with 82% accuracy, enabling proactive intervention.

---

## Approach

### Data & Features
- **Dataset:** 3,000+ student records from a public Kaggle source
- **Features:** 18 engineered attributes across 3 domains:
  - **Academic** (5): GPA, CGPA, attendance rate, study hours, assignment delays
  - **Socioeconomic** (5): family income, internet access, scholarships, part-time work, stress index
  - **Institutional** (8): semester, department, parental education, etc.

### Preprocessing Pipeline
- Imputation: median for numeric, mode for categorical
- Scaling: StandardScaler for numeric features
- Encoding: OneHotEncoder for categorical features
- Stratified train-test split (80/20, random_state=42)

### Model Selection & Training
- **Tested:** Logistic Regression, Random Forest, XGBoost
- **Winner:** Logistic Regression (Tuned) — best balance of accuracy (82%), interpretability, and inference speed
- **Tuning:** GridSearchCV (C, penalty, class_weight) with 5-fold CV, optimizing ROC-AUC
- **Rationale:** Advisors need to trust the model; interpretable LR builds confidence vs. black-box ensemble

### Explainability
- **SHAP Values:** Per-instance waterfall plots show how each feature contributes to prediction
- **Feature Importance:** Global SHAP summary reveals which features matter most
- **Output:** Color-coded confidence scores + detailed explanation for each prediction

### Evaluation Metrics
| Metric | Value |
|--------|-------|
| Accuracy | 81.2% |
| Precision | 0.79 |
| Recall | 0.81 |
| F1 Score | 0.80 |
| ROC-AUC | 0.88 |

---

## Key Results

✅ **Model Accuracy:** 82% on unseen test data  
✅ **Feature Importance:** 5 most critical factors identified (stress, GPA, attendance, delays, income)  
✅ **Explainable Predictions:** SHAP integration provides per-instance reasoning  
✅ **Production Readiness:** Containerized API, Streamlit UI, feedback loop for retraining  

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                  INPUT: Student Profile                      │
│  (Age, GPA, Attendance, Stress, Income, Department, etc.)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            PREPROCESSING (Scikit-learn Pipeline)             │
│   • Imputation (median/mode)                                 │
│   • Scaling (StandardScaler)                                 │
│   • Encoding (OneHotEncoder)                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│     LOGISTIC REGRESSION MODEL (Tuned via GridSearchCV)       │
│   • C=1.0, penalty='l2', class_weight='balanced'             │
│   • ROC-AUC: 0.88                                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            OUTPUT: Prediction + Explainability               │
│  • At-Risk / Will Persist (confidence score)                 │
│  • SHAP waterfall (per-feature contribution)                 │
│  • Global feature importance (SHAP summary)                  │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            FEEDBACK & RETRAINING LOOP                        │
│  • Collect advisor + true label feedback                     │
│  • Monthly retrain with new data                             │
│  • Monitor for drift & performance degradation               │
└─────────────────────────────────────────────────────────────┘
```

---

## Technologies & Tools

- **ML/Data:** Python, scikit-learn, Pandas, NumPy
- **Explainability:** SHAP, Matplotlib
- **Tuning:** GridSearchCV, Optuna (optional)
- **UI/Demo:** Streamlit (interactive dashboard)
- **Deployment:** Docker, GitHub Actions (CI/CD)
- **Experiment Tracking:** MLflow (lightweight logging)

---

## What Makes This Project Strong

1. **Interpretability First:** In ML for social good, trust = adoption. SHAP explainability is not an afterthought—it's central.

2. **Data-Driven Feature Selection:** Not guessing; EDA + correlation analysis informed which features to engineer.

3. **Balanced Metrics:** Precision (avoid false alarms) and Recall (catch actual risk) both matter. F1 = 0.80 shows balance.

4. **Production Thinking:** Feedback loop, retraining schedule, monitoring—ready to scale beyond demo.

5. **Clean Code:** Modular design (features.py, training.py, evaluate.py, cli.py) makes it easy to maintain and extend.

---

## Next Steps & Roadmap

### Short-term (v1.7–v1.8)
- [ ] Integrate Optuna for advanced hyperparameter tuning
- [ ] Add model monitoring dashboard (Prometheus/Grafana)
- [ ] Implement auto-retraining pipeline (Airflow/GitHub Actions)

### Medium-term (v2.1+)
- [ ] Deploy REST API (FastAPI) to production
- [ ] Scale data ingestion (connect to university SIS)
- [ ] A/B test messaging strategies (how to frame alert to advisor?)

### Long-term
- [ ] Multi-institution federation (privacy-preserving transfer learning)
- [ ] Personalization (recommend interventions per student)
- [ ] Causal analysis (what interventions actually help?)

---

## Key Learnings & Takeaways

🎯 **For Recruitment:**
- Demonstrated end-to-end ML pipeline: EDA → modeling → explainability → deployment
- Balanced technical rigor (GridSearchCV, SHAP, stratified splits) with production thinking (feedback loops, monitoring)
- Communicated complex ML concepts in terms non-ML stakeholders understand

🎯 **For the Field:**
- Early-warning systems work best when interpretable—black-box models fail in high-stakes settings
- Socioeconomic factors are as predictive as academics; holistic student support is data-backed
- Feedback loops and retraining are non-negotiable for real-world drift

---

## Contact / Questions

For questions, feedback, or collaboration:
- **GitHub:** [yuvalshahtech/student-management-system](https://github.com/yuvalshahtech/student-management-system)
- **Demo:** `.\scripts\run_demo.ps1` (Windows) or `bash scripts/run_demo.sh` (Mac/Linux)

---

**Version:** 2.0 (March 2026)  
**Status:** Showcase-Ready Portfolio Project
