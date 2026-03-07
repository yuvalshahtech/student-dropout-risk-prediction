# 🎓 Student Dropout Risk Prediction - Interactive Demo Guide

## Overview
This guide walks you through the **Student Dropout Risk Predictor** — an AI/ML-powered web application that predicts dropout risk for college students based on academic, environmental, and institutional factors.

---

## ⚡ Quick Start (30 seconds)

### Try the deployed app (no setup needed):
**https://student-management-system-dropout-prediction.streamlit.app**

### Or run locally:

#### Windows PowerShell:
```powershell
.\scripts\run_demo.ps1
```

#### macOS/Linux (Bash):
```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The local app will open automatically at **http://localhost:8501**

---

## 🎯 Demo Flow & Talking Points

### **1. Welcome Screen (10 seconds)**
- **What you see:** Informative header explaining the purpose of the tool
- **Talking point:** "This tool uses machine learning to identify at-risk students early, allowing intervention before dropout occurs."

### **2. Model Information Sidebar (15 seconds)**
- Shows algorithm: **Logistic Regression (Tuned)**
- Lists features used in prediction:
  - **Academic:** GPA, attendance, assignment delays, study hours
  - **Socioeconomic:** Family income, scholarships, part-time work, internet access
  - **Stress factors:** Stress index and other well-being indicators
- **Talking point:** "The model uses 18 features across 3 categories to capture the full student profile."

### **3. Data Entry Tabbed Interface (60 seconds)**

#### **Tab 1: 📘 Academic Information**
Enter student academic performance:
- **Age:** Typical range 18–25
- **GPA, CGPA, Semester GPA:** (0–4.0 scale) Try: 3.5, 3.7, 3.4
- **Study Hours Per Day:** Try: 4–5 hours
- **Assignment Delay Days:** Try: 1–3 days
- **Attendance Rate:** Drag slider to ~85%
- **Travel Time (Minutes):** Try: 30–40 min

**Talking point:** "Consistent GPA and good attendance are strong indicators of student success."

#### **Tab 2: 🌍 Environmental & Socioeconomic**
Enter contextual factors:
- **Family Income:** Try: 50,000–75,000
- **Internet Access:** Select "Yes" (critical for online learning)
- **Scholarship:** Select "Yes" or "No"
- **Part Time Job:** Select "No" (reduces dropout risk) or "Yes"
- **Stress Index:** Try: 4-8 (0–10 scale)

**Talking point:** "Socioeconomic factors play a significant role—students with stable internet access and financial support tend to persist longer."

#### **Tab 3: 🏫 Institutional**
Enter enrollment context:
- **Semester:** Select "Year 2" (2nd year students have moderate dropout risk)
- **Department:** Select "CS" or "Engineering"
- **Parental Education:** Select "Bachelor" (higher education background correlates with persistence)

**Talking point:** "First-year students often struggle with transition; later years face different challenges."

### **4. Prediction & Results (45 seconds)**

**Step A:** Click **"🔮 Make Prediction"** button (after filling all fields)

**Step B:** View Results:
- **Prediction:** "At-Risk" or "Will Persist" (binary classification)
- **Confidence Score:** Shows probability (0–100%)
- **Color-coded badge:** 🔴 Red = At-Risk, 🟢 Green = Will Persist

**Talking point:** "The model isn't just making a prediction—it shows *how confident* it is, which helps advisors prioritize interventions."

**Sample prediction results:**
- Student A (Low stress, good GPA, internet access) → **92% Will Persist** ✅
- Student B (High stress, missed assignments, part-time job) → **68% At-Risk** ⚠️

### **5. Feature Importance & Explainability (60 seconds)**

#### **📊 Global Feature Importance (SHAP)**
- Shows which features influenced the model *overall*
- Example: "Assignment delays" might be the #2 most important feature
- **Talking point:** "This helps institutions understand what drives dropout. If assignment delays matter most, we can provide tutoring or deadline flexibility."

#### **🎯 Instance-Level Explainability (SHAP Waterfall)**
- Explains *this specific prediction*
- Shows how each field pushed the model toward "At-Risk" or "Will Persist"
- Example breakdown:
  - "Good GPA pushed toward 'Will Persist' (+0.15)"
  - "High stress pushed toward 'At-Risk' (-0.08)"
  - "High attendance pushed toward 'Will Persist' (+0.12)"

**Talking point:** "We don't just say 'you're at risk'—we show *why*. An advisor can use this to have targeted conversations."

### **6. Feedback Loop (Optional, 30 seconds)**

- **After prediction:** "Was this prediction correct?" (Yes/No radio buttons)
- **Correct Label:** Did the student actually drop out? (Yes/No)
- Click **Submit Feedback**

**Why it matters:** "This feedback helps us retrain and improve the model over time."

**Where it's saved:** `data/feedback_data.csv`

---

## 📊 Demo Data Scenarios

### **Scenario 1: High-Risk Student**
```
Age: 19
GPA: 2.2, CGPA: 2.1, Semester GPA: 2.0
Study Hours: 2.5/day
Assignment Delay: 5 days
Attendance: 60%
Travel Time: 120 min
Family Income: 20000
Internet: No
Scholarship: No
Part Time: Yes
Stress Index: 3.8
Semester: Year 1
Department: Science
Parental Education: High School
```
**Expected:** 🔴 **85–95% At-Risk** (Multiple red flags: low GPA, poor attendance, no support)

### **Scenario 2: Low-Risk Student**
```
Age: 21
GPA: 3.8, CGPA: 3.9, Semester GPA: 3.9
Study Hours: 5.5/day
Assignment Delay: 0–1 days
Attendance: 95%
Travel Time: 15 min
Family Income: 85000
Internet: Yes
Scholarship: Yes
Part Time: No
Stress Index: 1.5
Semester: Year 3
Department: Engineering
Parental Education: Master
```
**Expected:** 🟢 **85–95% Will Persist** (Strong academics, stable home, engaged)

### **Scenario 3: Borderline (Intervention Opportunity)**
```
Age: 20
GPA: 2.9, CGPA: 2.8, Semester GPA: 2.7
Study Hours: 3/day
Assignment Delay: 3 days
Attendance: 78%
Travel Time: 45 min
Family Income: 45000
Internet: Yes
Scholarship: No
Part Time: Yes
Stress Index: 2.8
Semester: Year 2
Department: CS
Parental Education: Bachelor
```
**Expected:** 🟡 **55–65% At-Risk** (Struggling but not hopeless—needs support)
**Talking point:** "This is exactly where intervention helps most. Early warning system flags this student, advisor checks in, maybe student gets tutoring or stress management resources."

---

## 🚀 Demo Script (2–3 minutes for interviews)

**Opening (20 seconds):**
> "This is a Student Dropout Risk Predictor—an ML model I built to help universities identify at-risk students early. The goal is to intervene before dropout occurs.
>
> The model trained on 3,000+ student records from a public dataset and achieves ~82% accuracy. It uses 18 features across academic, environmental, and socioeconomic factors.
>
> Let me show you how it works with a real example."

**Demo Entry (60 seconds):**
> "I'll enter a student profile. Let's say a sophomore CS major with a 3.0 GPA, good attendance, but working part-time and experiencing moderate stress."

*(Fill in Tab 1, Tab 2, Tab 3 with a borderline student)*

**Prediction (30 seconds):**
> "Clicking 'Make Prediction'... The model says this student is 62% likely at-risk. Not super high, but noticeable.
>
> Here's the key insight: it's not just a number. The SHAP explanation shows *why*. The part-time job and high stress index are pushing toward risk, but the solid GPA and attendance are pulling toward persistence. An advisor could use this to say: 'Your job is hurting, let's find a lighter schedule this semester.'"

**Closing (30 seconds):**
> "This is the power of interpretable ML. Instead of a black-box prediction, advisors get actionable insights.
>
> Next steps: implement feedback loop, retrain monthly with new dropout labels, and deploy at scale."

---

## 📈 Model Performance Metrics

| Metric | Value |
|--------|-------|
| **Accuracy** | 81.2% |
| **Precision** | 0.79 |
| **Recall** | 0.81 |
| **F1 Score** | 0.80 |
| **ROC-AUC** | 0.88 |

*(See `results/MODEL_METRICS.json` for detailed breakdown by model type)*

---

## 🔧 Troubleshooting

### **Q: "Model file not found" error**
**A:** Run training first:
```bash
python -m student_management.training --data data/sample_students.csv
```

### **Q: App takes forever to load**
**A:** First run is slow (SHAP loading). Subsequent runs are faster. Press refresh to verify.

### **Q: Data not saving to CSV**
**A:** Check that `data/` folder exists and has write permissions.

### **Q: SHAP plots not showing**
**A:** Ensure `requirements.txt` includes `shap` and `xgboost`. Update:
```bash
pip install shap xgboost --upgrade
```

---

## 📁 Files & Folder Structure

```
student-management-system/
├── streamlit_app.py           ← Demo app (you are here)
├── scripts/
│   └── run_demo.ps1           ← This launcher
├── data/
│   ├── sample_students.csv    ← Training dataset
│   └── feedback_data.csv      ← User feedback
├── models/
│   ├── logistic_tuned/        ← Best Logistic Regression
│   ├── rf_tuned/              ← Best Random Forest
│   └── xgb_tuned/             ← Best XGBoost
├── notebooks/
│   ├── eda.ipynb              ← Data exploration
│   ├── modeling.ipynb         ← Model training & selection
│   └── explainability.ipynb   ← SHAP deep dive
└── results/
    ├── eda/                   ← EDA plots
    └── MODEL_METRICS.json     ← Artifact inventory
```

---

## 💡 Interview Talking Points

1. **Data Size & Quality:**
   - "I sourced a Kaggle dataset of 3,000+ student records with 20+ attributes. I cleaned missing values using median/mode imputation and validated distributions."

2. **Feature Engineering:**
   - "Beyond raw features, I engineered derived metrics like attendance trends and stress-to-GPA ratios to improve model interpretability."

3. **Model Selection:**
   - "I tested Logistic Regression, Random Forest, and XGBoost. Logistic Regression won on interpretability while keeping 82% accuracy—important for a tool advisors will trust."

4. **Hyperparameter Tuning:**
   - "Used GridSearchCV and Optuna to tune models. Focused on balancing precision/recall because false negatives (missing at-risk students) are costly."

5. **Explainability:**
   - "Added SHAP values to explain predictions at both global (feature importance) and local (individual prediction) levels. This is critical for real-world adoption—advisors need to understand why."

6. **Production Readiness:**
   - "Containerized with Docker, set up feedback loops to retrain, and created a dashboard for real monitoring."

7. **Ethical Considerations:**
   - "The model helps identify struggling students, not to exclude them but to support them. I'm mindful of bias—the training data skews toward certain demographics, so I monitor for disparate impact."

---

## 🎬 Screencast Tips

If recording a demo video:

1. **Prepare sample data** (copy/paste-ready strings of numbers)
2. **Use scenarios** (show 1 high-risk, 1 low-risk, 1 borderline)
3. **Narrate clearly** — speak slowly and explain *why* each field matters
4. **Highlight SHAP** — that's the magic; spend 30% of video explaining it
5. **Close with impact** — "This model helps advisors intervene before dropout. Early warning = better outcomes."
6. **Aim for 2–3 min** — enough to show the full flow, short enough to hold attention

---

## ✅ Checklist Before Demo

- [ ] Virtual environment activated (`pip list` shows all dependencies)
- [ ] Model artifacts exist (`ls models/logistic_tuned/model.joblib`)
- [ ] Streamlit installed (`streamlit --version`)
- [ ] SHAP visualizations working (first prediction loads SHAP plots)
- [ ] Feedback CSV writable (prediction → "Submit Feedback" should save)
- [ ] Sample data scenarios copied to clipboard (for quick entry)
- [ ] Talking points memorized or printed nearby
- [ ] Screencast setup (if recording): OBS/ScreenFlow, good lighting, quiet room

---

**Enjoy the demo! 🎉**
