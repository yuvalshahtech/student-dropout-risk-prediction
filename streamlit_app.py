import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import shap

st.set_page_config(
    page_title="Student Dropout Predictor",
    page_icon="🎓",
    layout="wide"
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "logistic_tuned", "model.joblib")
FEEDBACK_CSV = os.path.join(BASE_DIR, "data", "feedback_data.csv")
DATA_PATH = os.path.join(BASE_DIR, "data", "sample_students.csv")
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False
if "input_data" not in st.session_state:
    st.session_state.input_data = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False

@st.cache_data
def load_dataset():
    return pd.read_csv(DATA_PATH)
df = load_dataset()

with st.sidebar:
    st.header("Model Information")
    st.write("**Algorithm:** Logistic Regression")
    st.write("**Features Used:**")
    st.write("""
    • Academic performance  
    • Attendance behaviour  
    • Socioeconomic indicators  
    • Stress factors  
    """)
    st.markdown("---")
    st.write(
        "This tool predicts potential student dropout risk using machine learning."
    )

defaults = {
    "Age": df["Age"].median(),
    "GPA": df["GPA"].median(),
    "CGPA": df["CGPA"].median(),
    "Family_Income": df["Family_Income"].median(),
    "Stress_Index": df["Stress_Index"].median()
}

def get_stats(column):
    return (
        float(df[column].min()),
        float(df[column].max()),
        float(df[column].median())
    )

def dynamic_number_input(label, column_name):
    min_val, max_val, default = get_stats(column_name)
    st.markdown(f"*Leave the value as default ({default}) if unknown*")
    value = st.number_input(
        label,
        min_value=min_val,
        max_value=max_val * 2 if column_name not in [
            "GPA", "Semester_GPA", "CGPA", "Stress_Index"
        ] else max_val,
        value=default,
        help=f"Dataset Range: {min_val} - {max_val} (Leave as default if unknown)"
    )
    return value

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error("Model file not found!")
        st.stop()
    return joblib.load(MODEL_PATH)
pipeline = load_model()
classes = pipeline.named_steps["model"].classes_

if not os.path.exists(FEEDBACK_CSV):
    os.makedirs("data", exist_ok=True)
    headers = [
        "Age","Family_Income","Internet_Access","Study_Hours_per_Day",
        "Attendance_Rate","Assignment_Delay_Days","Travel_Time_Minutes",
        "Part_Time_Job","Scholarship","Stress_Index","GPA","Semester_GPA",
        "CGPA","Semester","Department","Parental_Education",
        "Prediction","Correct_Label","Probability","Timestamp"
    ]
    pd.DataFrame(columns=headers).to_csv(FEEDBACK_CSV, index=False)

st.markdown("""
<div style="
background-color:#EEF2FF;
padding:20px;
border-radius:12px;
border-left:6px solid #4F46E5;
color:#111827;
">
<h2>🎓 Student Dropout Risk Predictor</h2>
<p>AI-powered early warning system for student retention.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs([
    "📘 Academic",
    "🌍 Environment",
    "🏫 Institution"
])
st.markdown("<br>", unsafe_allow_html=True)
with tab1:
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        age = dynamic_number_input("Age", "Age")
        gpa = dynamic_number_input("GPA", "GPA")
        semester_gpa = dynamic_number_input("Semester GPA", "Semester_GPA")
    with row1_col2:
        cgpa = dynamic_number_input("CGPA", "CGPA")
        study_hours = dynamic_number_input("Study Hours Per Day", "Study_Hours_per_Day")
        assignment_delay = dynamic_number_input("Assignment Delay Days", "Assignment_Delay_Days")
    st.markdown("**Attendance Rate (%)**")
    attendance = st.slider("", 0, 100, 75)
    colA, colB = st.columns(2)
    with colA:
        travel_time = dynamic_number_input("Travel Time (Minutes)", "Travel_Time_Minutes")
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
with tab2:
    family_income = dynamic_number_input("Family Income", "Family_Income")
    internet = st.selectbox("Internet Access", ["Yes", "No"])
    scholarship = st.selectbox("Scholarship", ["Yes", "No"])
    part_time = st.selectbox("Part Time Job", ["Yes", "No"])
    stress = dynamic_number_input("Stress Index", "Stress_Index")
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
with tab3:
    semester = st.selectbox("Semester", ["Year 1", "Year 2", "Year 3", "Year 4"])
    department = st.selectbox(
        "Department",
        ["Science", "Arts", "Business", "CS", "Engineering"]
    )
    education = st.selectbox(
        "Parental Education",
        ["Unknown","HighSchool","Bachelor","Master","PhD"]
    )
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
confirm_data = st.checkbox("I confirm data is accurate")
left, center, right = st.columns([1,2,1])
with center:
    predict_clicked = st.button("🔍 Predict Dropout Risk", use_container_width=True)
if predict_clicked and confirm_data:
    input_data = pd.DataFrame([{
        "Age": age,
        "Family_Income": family_income,
        "Study_Hours_per_Day": study_hours,
        "Attendance_Rate": attendance,
        "Assignment_Delay_Days": assignment_delay,
        "Travel_Time_Minutes": travel_time,
        "Stress_Index": stress,
        "Internet_Access": internet,
        "Part_Time_Job": part_time,
        "Scholarship": scholarship,
        "GPA": gpa,
        "Semester_GPA": semester_gpa,
        "CGPA": cgpa,
        "Semester": semester,
        "Department": department,
        "Parental_Education": education

    }])
    binary_cols = ["Internet_Access", "Scholarship", "Part_Time_Job"]
    mapping = {"Yes": 1, "No": 0}
    input_data[binary_cols] = input_data[binary_cols].replace(mapping)
    input_data["Dept_Semester"] = input_data["Department"] + "_" + input_data["Semester"]
    input_data["Income_Stress_Ratio"] = input_data["Stress_Index"] / (input_data["Family_Income"] + 1)
    input_data["GPA_vs_CGPA"] = input_data["GPA"] - input_data["CGPA"]
    input_data["GPA_vs_SGPA"] = input_data["GPA"] - input_data["Semester_GPA"]
    input_data["Job_Stress_Interaction"] = input_data["Part_Time_Job"] * input_data["Stress_Index"]
    input_data["Student_Pressure_Index"] = (
        input_data["Assignment_Delay_Days"]
        + input_data["Travel_Time_Minutes"]
        + input_data["Part_Time_Job"]
        + input_data["Stress_Index"]
    ) / (input_data["Attendance_Rate"] + input_data["Study_Hours_per_Day"] + 0.01)
    input_data["Academic_Risk"] = (
        (input_data["Attendance_Rate"] < 75).astype(int)
        + (input_data["Study_Hours_per_Day"] < 2).astype(int)
        + (input_data["Assignment_Delay_Days"] > 5).astype(int)
    )
    prediction = pipeline.predict(input_data)[0]
    proba = pipeline.predict_proba(input_data)[0]
    class_index = list(classes).index(prediction)
    probability = round(proba[class_index] * 100, 2)
    st.session_state.input_data = input_data
    st.session_state.prediction = prediction
    st.session_state.probability = probability
    st.session_state.prediction_done = True
    st.session_state.feedback_submitted = False

if st.session_state.prediction_done:
    prediction = st.session_state.prediction
    probability = st.session_state.probability
    if prediction == 1:
        prediction_result = "⚠️ High Dropout Risk"
        color = "red"
    else:
        prediction_result = "✅ Low Dropout Risk"
        color = "green"
    bg_color = "#ffe6e6" if prediction == 1 else "#e6ffe6"
    st.markdown(f"""
    <div style="
    padding:22px;
    border-radius:12px;
    background-color:white;
    border-left:6px solid {'#DC2626' if prediction==1 else '#16A34A'};
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    ">
    <h3 style="color:{color};margin-bottom:5px;">{prediction_result}</h3>
    <p style="margin:0;color:#374151;">Model confidence: <b>{probability}%</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📊 Explain Model Decision"):
        @st.cache_data
        def run_shap(model_path, data_path, input_df):
            from student_management.explainability.shap_explainer import explain_user_input
            return explain_user_input(model_path, data_path, input_df)
        result = run_shap(
            MODEL_PATH,
            DATA_PATH,
            st.session_state.input_data
        )
        st.markdown("### Model Explanation")
        left, center, right = st.columns([1,2,1])
        with center:
            fig = plt.figure(figsize=(6,4))
            shap.waterfall_plot(
                shap.Explanation(
                    values=result["shap_values"],
                    base_values=result["expected_value"],
                    data=result["processed_features"],
                    feature_names=result["feature_names"]
                ),
                max_display=10
            )
            st.pyplot(fig)
        importance = pd.Series(
            abs(result["shap_values"]),
            index=result["feature_names"]
        ).sort_values(ascending=False).head(5)
        st.subheader("Top Factors Influencing Prediction")
        st.bar_chart(importance)
if st.session_state.prediction_done:
    st.markdown("---")
    st.subheader("Model Feedback")
    feedback = st.radio(
        "Was the model prediction correct?",
        ["Yes, it was correct", "No, it was wrong", "I don't know"],
        horizontal=True
    )
    submit_feedback = st.button(
        "Submit Feedback",
        disabled=st.session_state.feedback_submitted
    )
    if submit_feedback:
        if feedback == "I don't know":
            st.info("Feedback not recorded.")
        else:
            predicted = st.session_state.prediction
            if feedback == "Yes, it was correct":
                correct_label = predicted
            else:
                correct_label = 1 - predicted
            row = st.session_state.input_data.copy()
            row["Prediction"] = predicted
            row["Correct_Label"] = correct_label
            row["Probability"] = st.session_state.probability
            row["Timestamp"] = pd.Timestamp.now()
            row.to_csv(FEEDBACK_CSV, mode="a", header=False, index=False)
            st.success("Feedback recorded successfully!")
            st.session_state.feedback_submitted = True