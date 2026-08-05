import textwrap

import streamlit as st
import pandas as pd

from utils.loader import load_model
from utils.risk import get_risk_level, create_risk_gauge
from utils.ai_summary import render_ai_summary_section
from utils.theme import apply_assessment_theme


# ==================================================
# MODEL
# ==================================================

@st.cache_resource
def get_heart_model():
    return load_model("models/heart_disease_model.pkl")


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

def heart_page_test(general_data):

    heart_model = get_heart_model()

    apply_medical_theme()
    apply_assessment_theme()

    # Back Button
    if st.button("⬅️ Back to Assessment"):
        st.session_state.page = "assessment"
        st.rerun()

    # Header
    st.markdown(
        '<div class="title">❤️ Heart Disease Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A smart evaluation of your heart disease risk based on your health data</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Summary
    render_health_summary(general_data)

    st.divider()

    # Inputs
    st.subheader("❤️ Heart Related Information")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            chest_pain = st.selectbox(
                "Chest Pain Type",
                ["ATA", "NAP", "ASY", "TA"],
                key="heart_chest_pain"
            )

            resting_bp = st.number_input(
                "Resting Blood Pressure", 80, 200, 130,
                key="heart_resting_bp"
            )

            cholesterol = st.number_input(
                "Cholesterol", 85, 603, 237,
                key="heart_cholesterol"
            )

            # NOTE: FastingBS is numeric (0/1) in the trained
            # pipeline's preprocessor — only the display label is
            # "Normal"/"High", the stored value must stay 0/1.
            fasting_bs = st.selectbox(
                "Fasting Blood Sugar",
                [0, 1],
                format_func=lambda x: "Normal" if x == 0 else "High",
                help="High = fasting blood sugar > 120 mg/dl",
                key="heart_fasting_bs"
            )

        with col2:

            resting_ecg = st.selectbox(
                "Resting ECG",
                ["Normal", "LVH", "ST"],
                key="heart_resting_ecg"
            )

            max_hr = st.number_input(
                "Maximum Heart Rate", 60, 202, 138,
                key="heart_max_hr"
            )

            # NOTE: ExerciseAngina is categorical "N"/"Y" in the
            # trained pipeline — only the display label is "No"/"Yes".
            exercise_angina = st.selectbox(
                "Exercise-Induced Angina",
                ["N", "Y"],
                format_func=lambda x: "No" if x == "N" else "Yes",
                key="heart_exercise_angina"
            )

            oldpeak = st.number_input(
                "Oldpeak", -2.6, 6.2, 0.6, step=0.1,
                key="heart_oldpeak"
            )

            st_slope = st.selectbox(
                "ST Slope",
                ["Up", "Flat", "Down"],
                key="heart_st_slope"
            )

    st.write("")

    # ==================================================
    # Prediction
    # ==================================================

    if st.button("🔍 Analyze Heart Risk", use_container_width=True):

        data = pd.DataFrame({
            "Age": [general_data["age"]],
            "Sex": ["M" if general_data["gender"] == "Male" else "F"],
            "ChestPainType": [chest_pain],
            "RestingBP": [resting_bp],
            "Cholesterol": [cholesterol],
            "FastingBS": [fasting_bs],
            "RestingECG": [resting_ecg],
            "MaxHR": [max_hr],
            "ExerciseAngina": [exercise_angina],
            "Oldpeak": [oldpeak],
            "ST_Slope": [st_slope]
        })

        probability = heart_model.predict_proba(data)[0][1]
        prediction = heart_model.predict(data)[0]

        risk_level, message = get_risk_level(probability, "Heart Disease")

        patient_data = {
            "Age": general_data["age"],
            "Sex": "Male" if general_data["gender"] == "Male" else "Female",
            "Chest Pain Type": chest_pain,
            "Resting Blood Pressure": resting_bp,
            "Cholesterol": cholesterol,
            "Fasting Blood Sugar": "High" if fasting_bs == 1 else "Normal",
            "Resting ECG": resting_ecg,
            "Maximum Heart Rate": max_hr,
            "Exercise-Induced Angina": "Yes" if exercise_angina == "Y" else "No",
            "Oldpeak": oldpeak,
            "ST Slope": st_slope,
        }

        # Store everything so it survives reruns triggered by other
        # widgets on this page.
        st.session_state["heart_result"] = {
            "probability": probability,
            "risk_level": risk_level,
            "message": message,
            "prediction": prediction,
            "patient_data": patient_data,
        }

        # Clear any previously generated summary tied to older inputs
        st.session_state.pop("heart_ai_summary_en", None)
        st.session_state.pop("heart_ai_summary_ar", None)
        st.session_state.pop("heart_ai_summary_lang", None)

    # ==================================================
    # Display Result (persists across reruns)
    # ==================================================

    if "heart_result" in st.session_state:

        result = st.session_state["heart_result"]

        st.subheader("📊 Prediction Result")

        create_risk_gauge(result["probability"], "Heart Disease")
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
            🔴 Increased Heart Disease Risk Detected
            </h2>

            <p>
            The AI model detected patterns associated with increased heart disease risk.
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
                🟢 Low Heart Disease Risk Detected
                </h2>

                <p>
                The AI model did not detect strong indicators of heart disease.
                Continue maintaining a healthy lifestyle and regular checkups.
                </p>

                </div>
                """
            )

        st.divider()

        # -------------------------
        # AI Summary (styled card + translate + download report)
        # -------------------------

        render_ai_summary_section(
            page_key="heart",
            disease_label="Heart Disease",
            patient_data=result["patient_data"],
            probability=result["probability"],
            risk_level=result["risk_level"]
        )
