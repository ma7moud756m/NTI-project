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
def get_kidney_model():
    return load_model("models/kidney_model.pkl")


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

def kidney_page(general_data):

    kidney_model = get_kidney_model()

    apply_medical_theme()
    apply_assessment_theme()

    # Back Button
    if st.button("⬅️ Back to Assessment"):
        st.session_state.page = "assessment"
        st.rerun()

    # Header
    st.markdown(
        '<div class="title">🫘 Kidney Disease Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A smart evaluation of your kidney disease risk based on your health data</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Health Summary
    render_health_summary(general_data)

    st.divider()

    # ==================================================
    # INPUTS
    # ==================================================

    st.subheader("🩺 Kidney Related Information")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🧪 Urine Analysis",
        "🧬 Medical History",
        "🔬 Blood Tests",
        "🩺 Clinical Signs"
    ])

    # ============================
    # TAB 1 - URINE
    # ============================

    with tab1:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                specific_gravity = st.selectbox(
                    "Specific Gravity",
                    [1.005, 1.010, 1.015, 1.020, 1.025],
                    key="kidney_specific_gravity"
                )

                albumin = st.selectbox(
                    "Albumin",
                    [0, 1, 2, 3, 4, 5],
                    key="kidney_albumin"
                )

                sugar = st.selectbox(
                    "Sugar",
                    [0, 1, 2, 3, 4, 5],
                    key="kidney_sugar"
                )

                red_blood_cells = st.selectbox(
                    "Red Blood Cells",
                    ["normal", "abnormal"],
                    key="kidney_rbc"
                )

            with col2:

                pus_cell = st.selectbox(
                    "Pus Cell",
                    ["normal", "abnormal"],
                    key="kidney_pus_cell"
                )

                pus_cell_clumps = st.selectbox(
                    "Pus Cell Clumps",
                    ["notpresent", "present"],
                    key="kidney_pus_cell_clumps"
                )

                bacteria = st.selectbox(
                    "Bacteria",
                    ["notpresent", "present"],
                    key="kidney_bacteria"
                )

    # ============================
    # TAB 2 - MEDICAL HISTORY
    # ============================

    with tab2:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                hypertension = st.selectbox(
                    "Hypertension",
                    ["yes", "no"],
                    key="kidney_hypertension"
                )

                diabetes_mellitus = st.selectbox(
                    "Diabetes Mellitus",
                    ["yes", "no"],
                    key="kidney_diabetes_mellitus"
                )

            with col2:

                coronary_artery_disease = st.selectbox(
                    "Coronary Artery Disease",
                    ["no", "yes"],
                    key="kidney_cad"
                )

    # ============================
    # TAB 3 - BLOOD TESTS
    # ============================

    with tab3:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                blood_pressure = st.number_input(
                    "Blood Pressure", 50, 200, 80,
                    key="kidney_bp"
                )

                blood_glucose_random = st.number_input(
                    "Blood Glucose Random", 20, 500, 120,
                    key="kidney_glucose_random"
                )

                blood_urea = st.number_input(
                    "Blood Urea", 1.0, 400.0, 40.0,
                    key="kidney_blood_urea"
                )

                serum_creatinine = st.number_input(
                    "Serum Creatinine", 0.1, 80.0, 1.2,
                    key="kidney_creatinine"
                )

                sodium = st.number_input(
                    "Sodium", 1.0, 200.0, 138.0,
                    key="kidney_sodium"
                )

            with col2:

                potassium = st.number_input(
                    "Potassium", 1.0, 50.0, 4.4,
                    key="kidney_potassium"
                )

                hemoglobin = st.number_input(
                    "Hemoglobin", 1.0, 20.0, 13.0,
                    key="kidney_hemoglobin"
                )

                packed_cell_volume = st.number_input(
                    "Packed Cell Volume", 1.0, 60.0, 40.0,
                    key="kidney_pcv"
                )

                white_blood_cell_count = st.number_input(
                    "White Blood Cell Count", 1000.0, 30000.0, 8000.0,
                    key="kidney_wbc"
                )

                red_blood_cell_count = st.number_input(
                    "Red Blood Cell Count", 1.0, 10.0, 5.0,
                    key="kidney_rbc_count"
                )

    # ============================
    # TAB 4 - CLINICAL SIGNS
    # ============================

    with tab4:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                appetite = st.selectbox(
                    "Appetite",
                    ["good", "poor"],
                    key="kidney_appetite"
                )

                pedal_edema = st.selectbox(
                    "Pedal Edema",
                    ["no", "yes"],
                    key="kidney_pedal_edema"
                )

            with col2:

                anemia = st.selectbox(
                    "Anemia",
                    ["no", "yes"],
                    key="kidney_anemia"
                )

    st.write("")

    # ============================
    # PREDICTION
    # ============================

    if st.button("🔍 Analyze Kidney Risk", use_container_width=True):

        data = pd.DataFrame({
            "age": [general_data["age"]],
            "blood_pressure": [blood_pressure],
            "specific_gravity": [specific_gravity],
            "albumin": [albumin],
            "sugar": [sugar],
            "red_blood_cells": [red_blood_cells],
            "pus_cell": [pus_cell],
            "pus_cell_clumps": [pus_cell_clumps],
            "bacteria": [bacteria],
            "blood_glucose_random": [blood_glucose_random],
            "blood_urea": [blood_urea],
            "serum_creatinine": [serum_creatinine],
            "sodium": [sodium],
            "potassium": [potassium],
            "hemoglobin": [hemoglobin],
            "packed_cell_volume": [packed_cell_volume],
            "white_blood_cell_count": [white_blood_cell_count],
            "red_blood_cell_count": [red_blood_cell_count],
            "hypertension": [hypertension],
            "diabetes_mellitus": [diabetes_mellitus],
            "coronary_artery_disease": [coronary_artery_disease],
            "appetite": [appetite],
            "pedal_edema": [pedal_edema],
            "anemia": [anemia]
        })

        if hasattr(kidney_model, "predict_proba"):
            probability = kidney_model.predict_proba(data)[0][1]
        else:
            probability = float(kidney_model.predict(data)[0])

        prediction = 1 if probability >= 0.5 else 0

        risk_level, message = get_risk_level(probability, "Kidney Disease")

        patient_data = {
            "Age": general_data["age"],
            "Blood Pressure": blood_pressure,
            "Specific Gravity": specific_gravity,
            "Albumin": albumin,
            "Sugar": sugar,
            "Blood Glucose Random": blood_glucose_random,
            "Blood Urea": blood_urea,
            "Serum Creatinine": serum_creatinine,
            "Sodium": sodium,
            "Potassium": potassium,
            "Hemoglobin": hemoglobin,
            "Hypertension": hypertension,
            "Diabetes Mellitus": diabetes_mellitus,
            "Coronary Artery Disease": coronary_artery_disease,
            "Appetite": appetite,
            "Pedal Edema": pedal_edema,
            "Anemia": anemia,
        }

        # Store everything so it survives reruns triggered by other
        # widgets on this page.
        st.session_state["kidney_result"] = {
            "probability": probability,
            "prediction": prediction,
            "risk_level": risk_level,
            "message": message,
            "patient_data": patient_data,
        }

        # Clear any previously generated summary tied to older inputs
        st.session_state.pop("kidney_ai_summary_en", None)
        st.session_state.pop("kidney_ai_summary_ar", None)
        st.session_state.pop("kidney_ai_summary_lang", None)

    # ============================
    # DISPLAY RESULT (persists across reruns)
    # ============================

    if "kidney_result" in st.session_state:

        result = st.session_state["kidney_result"]

        st.subheader("📊 Prediction Result")

        create_risk_gauge(result["probability"], "Kidney Disease")
        st.info(result["message"])

        # -------------------------
        # Final Result Card
        # -------------------------

        if "High" in result["risk_level"] or "Moderate" in result["risk_level"]:

            render_card(
                "Final Result",
                """
                <div style="text-align:center;">

                <h2 style="color:#dc2626;">
                🔴 Increased Kidney Disease Risk Detected
                </h2>

                <p>
                The AI model detected patterns associated with increased kidney disease risk.
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
                🟢 Low Kidney Disease Risk Detected
                </h2>

                <p>
                The AI model did not detect strong indicators of kidney disease.
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
            page_key="kidney",
            disease_label="Kidney Disease",
            patient_data=result["patient_data"],
            probability=result["probability"],
            risk_level=result["risk_level"]
        )
