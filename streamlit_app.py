import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import shap

# ---------------------------------------------------------------------------
# Heroicons SVG library (outline, 24x24) — https://heroicons.com
# ---------------------------------------------------------------------------
HERO = {
    "academic_cap": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5"/></svg>',
    "book_open": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"/></svg>',
    "globe": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5a17.92 17.92 0 0 1-8.716-2.247m0 0A8.966 8.966 0 0 1 3 12c0-1.264.26-2.467.732-3.559"/></svg>',
    "building_library": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0 0 12 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75Z"/></svg>',
    "magnifying_glass": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>',
    "exclamation_triangle": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"/></svg>',
    "check_circle": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/></svg>',
    "chart_bar": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z"/></svg>',
    "information_circle": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"/></svg>',
    "cpu_chip": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3M21 8.25h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3M21 15.75h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 0 0 2.25-2.25V6.75a2.25 2.25 0 0 0-2.25-2.25H6.75A2.25 2.25 0 0 0 4.5 6.75v10.5a2.25 2.25 0 0 0 2.25 2.25Zm.75-12h9v9h-9v-9Z"/></svg>',
    "clipboard_document_list": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15a2.25 2.25 0 0 1 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z"/></svg>',
    "shield_check": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"/></svg>',
    "chat_bubble_left_right": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155"/></svg>',
    "hand_thumb_up": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M6.633 10.25c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282m0 0h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23H5.904M14.25 9h2.25M5.904 18.5c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 0 1-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 9.953 4.167 9.5 5 9.5h1.053c.472 0 .745.556.5.96a8.958 8.958 0 0 0-1.302 4.665c0 1.194.232 2.333.654 3.375Z"/></svg>',
    "paper_airplane": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"/></svg>',
    "light_bulb": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="{w}" height="{h}" style="{s}"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18"/></svg>',
}


def icon(name, w=20, h=20, color=None, style="vertical-align:middle;margin-right:6px;"):
    """Render a Heroicon SVG inline with optional color override."""
    svg = HERO[name].format(w=w, h=h, s=style)
    if color:
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    return svg


st.set_page_config(
    page_title="Student Dropout Predictor",
    page_icon="graduation_cap",
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
.icon-inline svg { vertical-align: middle; margin-right: 6px; }
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
    st.markdown(
        f'<h3>{icon("cpu_chip", 22, 22, "#4F46E5")} Model Information</h3>',
        unsafe_allow_html=True,
    )
    st.write("**Algorithm:** Logistic Regression")
    st.markdown(
        f'{icon("clipboard_document_list", 18, 18, "#6366F1")} **Features Used:**',
        unsafe_allow_html=True,
    )
    st.write("""
    - Academic performance  
    - Attendance behaviour  
    - Socioeconomic indicators  
    - Stress factors  
    """)
    st.markdown("---")
    st.markdown(
        f'{icon("information_circle", 18, 18, "#6B7280")} '
        "This tool predicts potential student dropout risk using machine learning.",
        unsafe_allow_html=True,
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

st.markdown(f"""
<div style="
background-color:#EEF2FF;
padding:20px;
border-radius:12px;
border-left:6px solid #4F46E5;
color:#111827;
">
<h2>{icon("academic_cap", 28, 28, "#4F46E5")} Student Dropout Risk Predictor</h2>
<p>{icon("light_bulb", 16, 16, "#6366F1")} AI-powered early warning system for student retention.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

academic_label = f'{icon("book_open", 16, 16, "#4F46E5")} Academic'
environment_label = f'{icon("globe", 16, 16, "#059669")} Environment'
institution_label = f'{icon("building_library", 16, 16, "#7C3AED")} Institution'

tab1, tab2, tab3 = st.tabs([
    "Academic",
    "Environment",
    "Institution"
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
    predict_clicked = st.button("Predict Dropout Risk", use_container_width=True, type="primary", icon=":material/search:")
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
        prediction_label = "High Dropout Risk"
        color = "red"
        result_icon = icon("exclamation_triangle", 22, 22, "#DC2626")
    else:
        prediction_label = "Low Dropout Risk"
        color = "green"
        result_icon = icon("check_circle", 22, 22, "#16A34A")
    st.markdown(f"""
    <div style="
    padding:22px;
    border-radius:12px;
    background-color:white;
    border-left:6px solid {'#DC2626' if prediction==1 else '#16A34A'};
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    ">
    <h3 style="color:{color};margin-bottom:5px;">{result_icon} {prediction_label}</h3>
    <p style="margin:0;color:#374151;">{icon("shield_check", 16, 16, "#374151")} Model confidence: <b>{probability}%</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Explain Model Decision", icon=":material/analytics:"):
        @st.cache_data
        def run_shap(model_path, data_path, input_df):
            from student_management.explainability.shap_explainer import explain_user_input
            return explain_user_input(model_path, data_path, input_df)
        result = run_shap(
            MODEL_PATH,
            DATA_PATH,
            st.session_state.input_data
        )
        st.markdown(
            f'<h3>{icon("light_bulb", 22, 22, "#F59E0B")} Model Explanation</h3>',
            unsafe_allow_html=True,
        )
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
        st.markdown(
            f'<h4>{icon("chart_bar", 20, 20, "#4F46E5")} Top Factors Influencing Prediction</h4>',
            unsafe_allow_html=True,
        )
        st.bar_chart(importance)
if st.session_state.prediction_done:
    st.markdown("---")
    st.markdown(
        f'<h3>{icon("chat_bubble_left_right", 22, 22, "#4F46E5")} Model Feedback</h3>',
        unsafe_allow_html=True,
    )
    feedback = st.radio(
        "Was the model prediction correct?",
        ["Yes, it was correct", "No, it was wrong", "I don't know"],
        horizontal=True
    )
    submit_feedback = st.button(
        "Submit Feedback",
        disabled=st.session_state.feedback_submitted,
        icon=":material/send:",
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