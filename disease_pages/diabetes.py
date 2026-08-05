import textwrap

import streamlit as st
import pandas as pd

from utils.loader import load_model
from utils.risk import get_risk_level, create_risk_gauge
from utils.ai_summary import render_ai_summary_section
from utils.theme import apply_assessment_theme


@st.cache_resource
def get_diabetes_model():
    return load_model("models/Diabetes_Pipeline.pkl")


# ==================================================
# THEME
# ==================================================

def apply_medical_theme():

    st.markdown(
        """
        <style>

        .stApp{
            background-color:#F8FCFF;
        }

        .title{
            color:#0077B6;
            font-size:38px;
            font-weight:bold;
            text-align:center;
            margin-bottom:5px;
        }

        .subtitle{
            color:#4A4A4A;
            font-size:16px;
            text-align:center;
            margin-bottom:25px;
        }

        .card{
            background:#EAF7FF;
            padding:20px;
            border-radius:20px;
            border:1px solid #BDE3F7;
            margin-bottom:15px;
        }

        .card h3{
            color:#0077B6;
            margin-top:0px;
        }

        .summary-card{
            background:#F4FBFF;
            padding:15px;
            border-radius:16px;
            border:1px solid #D6EEFB;
            text-align:center;
            margin-bottom:10px;
        }

        .summary-card h4{
            color:#0077B6;
            margin:0px;
            font-size:14px;
        }

        .summary-card p{
            color:#333;
            font-size:20px;
            font-weight:bold;
            margin:5px 0px 0px 0px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# CARD
# ==================================================

def render_card(title, content):

    clean_content = textwrap.dedent(content).strip()

    card_html = (
        f'<div class="card"><h3>{title}</h3>{clean_content}</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)


# ==================================================
# HEALTH SUMMARY
# ==================================================

def render_health_summary(general_data):

    st.subheader("📋 Your Health Summary")

    col1, col2, col3, col4 = st.columns(4)

    summary_items = [
        ("Age", general_data.get("age", "-")),
        ("BMI", general_data.get("bmi", "-")),
        ("Smoking Status", general_data.get("smoking_status", "-")),
        ("Physical Activity", general_data.get("physical_activity", "-")),
    ]

    for col, (label, value) in zip((col1, col2, col3, col4), summary_items):

        with col:

            card_html = (
                f'<div class="summary-card"><h4>{label}</h4><p>{value}</p></div>'
            )

            st.markdown(card_html, unsafe_allow_html=True)

    st.write("")


# ==================================================
# MAIN PAGE
# ==================================================

def diabetes_page(general_data):

    diabetes_model = get_diabetes_model()

    apply_medical_theme()
    apply_assessment_theme()

    # ---------- Back Button ----------
    if st.button("⬅️ Back to Assessment"):
        st.session_state.page = "assessment"
        st.rerun()

    # ---------- Header ----------
    st.markdown('<div class="title">🩸 Diabetes Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">A smart evaluation of your diabetes risk based on your health data</div>', unsafe_allow_html=True)

    st.write("")

    # ---------- Health Summary ----------
    render_health_summary(general_data)

    st.divider()

    # ---------- Additional Inputs (organized in tabs) ----------
    st.subheader("🩺 Diabetes Related Information")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Demographics",
        "🏃 Lifestyle",
        "🧬 Medical History",
        "📏 Body & Vitals",
        "🧪 Lab Results"
    ])

    with tab1:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"],
                    key="diabetes_gender"
                )

                ethnicity = st.selectbox(
                    "Ethnicity",
                    ["Asian", "White", "Hispanic", "Black", "Other"],
                    key="diabetes_ethnicity"
                )

                education_level = st.selectbox(
                    "Education Level",
                    ["Highschool", "Graduate", "Postgraduate", "No formal"],
                    key="diabetes_education"
                )

            with col2:

                income_level = st.selectbox(
                    "Income Level",
                    ["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"],
                    key="diabetes_income"
                )

                employment_status = st.selectbox(
                    "Employment Status",
                    ["Employed", "Unemployed", "Retired", "Student"],
                    key="diabetes_employment"
                )

                smoking_status = st.selectbox(
                    "Smoking Status",
                    ["Never", "Former", "Current"],
                    key="diabetes_smoking"
                )

    with tab2:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                physical_activity_minutes_per_week = st.number_input(
                    "Physical Activity (minutes/week)",
                    0, 1000, 150,
                    key="diabetes_activity_minutes"
                )

                diet_score = st.slider(
                    "Diet Quality Score (0 = poor, 10 = excellent)",
                    0, 10, 5,
                    key="diabetes_diet_score"
                )

            with col2:

                sleep_hours_per_day = st.number_input(
                    "Sleep Hours per Day",
                    0.0, 24.0, 7.0, step=0.5,
                    key="diabetes_sleep"
                )

                alcohol_consumption_per_week = st.number_input(
                    "Alcohol Consumption (units/week)",
                    0, 50, 0,
                    key="diabetes_alcohol"
                )

                screen_time_hours_per_day = st.number_input(
                    "Screen Time Hours per Day",
                    0.0, 24.0, 4.0, step=0.5,
                    key="diabetes_screen_time"
                )

    with tab3:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                family_history_diabetes = st.selectbox(
                    "Family History of Diabetes",
                    [0, 1],
                    format_func=lambda x: "No" if x == 0 else "Yes",
                    key="diabetes_family_history"
                )

                hypertension_history = st.selectbox(
                    "History of Hypertension",
                    [0, 1],
                    format_func=lambda x: "No" if x == 0 else "Yes",
                    key="diabetes_hypertension"
                )

            with col2:

                cardiovascular_history = st.selectbox(
                    "History of Cardiovascular Disease",
                    [0, 1],
                    format_func=lambda x: "No" if x == 0 else "Yes",
                    key="diabetes_cardio"
                )

    with tab4:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                waist_to_hip_ratio = st.number_input(
                    "Waist-to-Hip Ratio",
                    0.5, 1.5, 0.85, step=0.01,
                    key="diabetes_whr"
                )

                systolic_bp = st.number_input(
                    "Systolic Blood Pressure (mmHg)",
                    70, 250, 120,
                    key="diabetes_systolic"
                )

            with col2:

                diastolic_bp = st.number_input(
                    "Diastolic Blood Pressure (mmHg)",
                    40, 150, 80,
                    key="diabetes_diastolic"
                )

                heart_rate = st.number_input(
                    "Resting Heart Rate (bpm)",
                    40, 200, 75,
                    key="diabetes_heart_rate"
                )

    with tab5:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                cholesterol_total = st.number_input(
                    "Total Cholesterol (mg/dL)",
                    100, 400, 180,
                    key="diabetes_chol_total"
                )

                hdl_cholesterol = st.number_input(
                    "HDL Cholesterol (mg/dL)",
                    10, 150, 50,
                    key="diabetes_hdl"
                )

                ldl_cholesterol = st.number_input(
                    "LDL Cholesterol (mg/dL)",
                    30, 300, 100,
                    key="diabetes_ldl"
                )

                triglycerides = st.number_input(
                    "Triglycerides (mg/dL)",
                    30, 600, 130,
                    key="diabetes_triglycerides"
                )

            with col2:

                glucose_fasting = st.number_input(
                    "Fasting Glucose (mg/dL)",
                    50, 400, 95,
                    key="diabetes_glucose_fasting"
                )

                glucose_postprandial = st.number_input(
                    "Postprandial Glucose (mg/dL)",
                    50, 500, 120,
                    key="diabetes_glucose_pp"
                )

                insulin_level = st.number_input(
                    "Insulin Level (µU/mL)",
                    1.0, 300.0, 15.0,
                    key="diabetes_insulin"
                )

                hba1c = st.number_input(
                    "HbA1c (%)",
                    3.0, 15.0, 5.4, step=0.1,
                    key="diabetes_hba1c"
                )

    st.write("")

    # ==================================================
    # Prediction
    # ==================================================

    if st.button("🔍 Analyze Diabetes Risk", use_container_width=True):

        data = pd.DataFrame({
            "age": [general_data["age"]],
            "gender": [gender],
            "ethnicity": [ethnicity],
            "education_level": [education_level],
            "income_level": [income_level],
            "employment_status": [employment_status],
            "smoking_status": [smoking_status],
            "alcohol_consumption_per_week": [alcohol_consumption_per_week],
            "physical_activity_minutes_per_week": [physical_activity_minutes_per_week],
            "diet_score": [diet_score],
            "sleep_hours_per_day": [sleep_hours_per_day],
            "screen_time_hours_per_day": [screen_time_hours_per_day],
            "family_history_diabetes": [family_history_diabetes],
            "hypertension_history": [hypertension_history],
            "cardiovascular_history": [cardiovascular_history],
            "bmi": [general_data["bmi"]],
            "waist_to_hip_ratio": [waist_to_hip_ratio],
            "systolic_bp": [systolic_bp],
            "diastolic_bp": [diastolic_bp],
            "heart_rate": [heart_rate],
            "cholesterol_total": [cholesterol_total],
            "hdl_cholesterol": [hdl_cholesterol],
            "ldl_cholesterol": [ldl_cholesterol],
            "triglycerides": [triglycerides],
            "glucose_fasting": [glucose_fasting],
            "glucose_postprandial": [glucose_postprandial],
            "insulin_level": [insulin_level],
            "hba1c": [hba1c]
        })

        probability = diabetes_model.predict_proba(data)[0][1]
        prediction = diabetes_model.predict(data)[0]

        risk_level, message = get_risk_level(probability, "Diabetes")

        patient_data = {
            "Age": general_data["age"],
            "Gender": gender,
            "BMI": general_data["bmi"],
            "Waist-to-Hip Ratio": waist_to_hip_ratio,
            "Fasting Glucose": glucose_fasting,
            "Postprandial Glucose": glucose_postprandial,
            "HbA1c": hba1c,
            "Physical Activity (min/week)": physical_activity_minutes_per_week,
            "Smoking Status": smoking_status,
            "Family History of Diabetes": "Yes" if family_history_diabetes == 1 else "No",
            "Hypertension History": "Yes" if hypertension_history == 1 else "No",
            "Cardiovascular History": "Yes" if cardiovascular_history == 1 else "No",
        }

        # Store everything so it survives reruns triggered by other
        # widgets on this page.
        st.session_state["diabetes_result"] = {
            "probability": probability,
            "risk_level": risk_level,
            "message": message,
            "prediction": prediction,
            "patient_data": patient_data,
        }

        # Clear any previously generated summary tied to older inputs
        st.session_state.pop("diabetes_ai_summary_en", None)
        st.session_state.pop("diabetes_ai_summary_ar", None)
        st.session_state.pop("diabetes_ai_summary_lang", None)

    # ==================================================
    # Display Result (persists across reruns)
    # ==================================================

    if "diabetes_result" in st.session_state:

        result = st.session_state["diabetes_result"]

        st.subheader("📊 Prediction Result")

        create_risk_gauge(result["probability"], "Diabetes")
        st.info(result["message"])

        # -------------------------
        # Final Prediction Card
        # -------------------------

        if "High" in result["risk_level"] or "Moderate" in result["risk_level"]:

            render_card(
                "Final Result",
                """
                <div style="text-align:center;">

                <h2 style="color:#dc2626;">
                🔴 Increased Diabetes Risk Detected
                </h2>

                <p>
                The model detected patterns associated with increased diabetes risk.
                Please consult a healthcare professional for further evaluation.
                </p>

                </div>
                """
            )


        else:

            render_card(
                "Final Result",
                """
                <div style="text-align:center;">

                <h2 style="color:#16a34a;">
                🟢 No Significant Diabetes Risk Detected
                </h2>

                <p>
                No strong diabetes-related patterns were detected.
                </p>

                </div>
                """
            )


        st.divider()


        # -------------------------
        # AI Summary (styled card + translate + download report)
        # -------------------------

        render_ai_summary_section(
            page_key="diabetes",
            disease_label="Diabetes",
            patient_data=result["patient_data"],
            probability=result["probability"],
            risk_level=result["risk_level"]
        )
