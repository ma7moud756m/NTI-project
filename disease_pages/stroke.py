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
def get_stroke_model():
    return load_model("models/stroke_model.pkl")


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

def stroke_page(general_data):

    stroke_model = get_stroke_model()

    apply_medical_theme()
    apply_assessment_theme()

    # ---------- Back Button ----------
    if st.button("⬅️ Back to Assessment"):
        st.session_state.page = "assessment"
        st.rerun()

    # ---------- Header ----------
    st.markdown(
        '<div class="title">🧠 Stroke Risk Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A smart evaluation of your stroke risk based on your health data</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # ---------- Health Summary ----------
    render_health_summary(general_data)

    st.divider()

    # ---------- Additional Inputs ----------
    st.subheader("🩺 Stroke Related Information")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            hypertension = st.selectbox(
                "Hypertension",
                [0, 1],
                format_func=lambda x: "No" if x == 0 else "Yes",
                key="stroke_hypertension"
            )

            heart_disease = st.selectbox(
                "Heart Disease",
                [0, 1],
                format_func=lambda x: "No" if x == 0 else "Yes",
                key="stroke_heart"
            )

            glucose = st.number_input(
                "Average Glucose Level",
                50, 300, 100,
                key="stroke_glucose"
            )

        with col2:

            ever_married = st.selectbox(
                "Ever Married",
                ["Yes", "No"],
                key="stroke_married"
            )

            work_type = st.selectbox(
                "Work Type",
                ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
                key="stroke_work"
            )

            residence = st.selectbox(
                "Residence Type",
                ["Urban", "Rural"],
                key="stroke_residence"
            )

    st.write("")

    # ==================================================
    # Prediction
    # ==================================================

    if st.button("🔍 Analyze Stroke Risk", use_container_width=True):

        data = pd.DataFrame({
            "gender": [general_data["gender"]],
            "age": [general_data["age"]],
            "hypertension": [hypertension],
            "heart_disease": [heart_disease],
            "ever_married": [ever_married],
            "work_type": [work_type],
            "Residence_type": [residence],
            "avg_glucose_level": [glucose],
            "bmi": [general_data["bmi"]],
            "smoking_status": [general_data["smoking_status"]]
        })

        probability = stroke_model.predict_proba(data)[0][1]
        prediction = stroke_model.predict(data)[0]

        risk_level, message = get_risk_level(probability, "Stroke")

        patient_data = {
            "Age": general_data["age"],
            "Gender": general_data["gender"],
            "BMI": general_data["bmi"],
            "Smoking Status": general_data["smoking_status"],
            "Hypertension": "Yes" if hypertension == 1 else "No",
            "Heart Disease": "Yes" if heart_disease == 1 else "No",
            "Average Glucose Level": glucose,
            "Ever Married": ever_married,
            "Work Type": work_type,
            "Residence Type": residence,
        }

        # Store everything so it survives reruns triggered by other
        # widgets on this page.
        st.session_state["stroke_result"] = {
            "probability": probability,
            "risk_level": risk_level,
            "message": message,
            "prediction": prediction,
            "patient_data": patient_data,
        }

        # Clear any previously generated summary tied to older inputs
        st.session_state.pop("stroke_ai_summary_en", None)
        st.session_state.pop("stroke_ai_summary_ar", None)
        st.session_state.pop("stroke_ai_summary_lang", None)

    # ==================================================
    # Display Result (persists across reruns)
    # ==================================================

    if "stroke_result" in st.session_state:

        result = st.session_state["stroke_result"]

        st.subheader("📊 Prediction Result")

        create_risk_gauge(result["probability"], "Stroke")
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
                🔴 Increased Stroke Risk Detected
                </h2>

                <p>
                The AI model detected patterns associated with increased stroke risk.
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
                🟢 Low Stroke Risk Detected
                </h2>

                <p>
                The AI model did not detect strong indicators of stroke risk.
                Continue maintaining a healthy lifestyle and regular medical checkups.
                </p>

                </div>
                """
            )

        st.divider()

        # -------------------------
        # AI Summary (styled card + translate + download report)
        # -------------------------

        render_ai_summary_section(
            page_key="stroke",
            disease_label="Stroke",
            patient_data=result["patient_data"],
            probability=result["probability"],
            risk_level=result["risk_level"]
        )
