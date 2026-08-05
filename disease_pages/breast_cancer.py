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
def get_breast_model():
    return load_model("models/breast_logistic.pkl")


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
            margin:5px 0px;
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

    st.markdown(
        f"""
        <div class="card">

            <h3>{title}</h3>

            {clean_content}

        </div>
        """,
        unsafe_allow_html=True
    )



# ==================================================
# HEALTH SUMMARY
# ==================================================

def render_health_summary(general_data):

    st.subheader("📋 Your Health Summary")

    col1, col2, col3, col4 = st.columns(4)


    items = [

        ("Age", general_data.get("age","-")),

        ("BMI", general_data.get("bmi","-")),

        ("Smoking Status",
         general_data.get("smoking_status","-")),

        ("Physical Activity",
         general_data.get("physical_activity","-"))

    ]


    for col,(label,value) in zip(
        [col1,col2,col3,col4],
        items
    ):

        with col:

            st.markdown(
                f"""
                <div class="summary-card">

                <h4>{label}</h4>

                <p>{value}</p>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.write("")



# ==================================================
# MAIN PAGE
# ==================================================

def breast_cancer_page(general_data):


    breast_model = get_breast_model()

    apply_medical_theme()
    apply_assessment_theme()



    if st.button("⬅️ Back to Assessment"):

        st.session_state.page="assessment"

        st.rerun()



    st.markdown(
        '<div class="title">🎗 Breast Cancer Risk Assessment</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="subtitle">

        Smart breast cancer risk evaluation
        based on tumor measurements.

        </div>
        """,
        unsafe_allow_html=True
    )



    render_health_summary(general_data)


    st.divider()


    st.subheader("🎗 Breast Cancer Measurements")


    tab1, tab2, tab3 = st.tabs(
        [
            "📏 Mean Features",
            "📊 Standard Error",
            "⚠️ Worst Features"
        ]
    )

# ==================================================
# TAB 1 : MEAN FEATURES
# ==================================================

    with tab1:

        with st.container(border=True):

            col1, col2 = st.columns(2)


            with col1:

                radius_mean = st.number_input(
                    "Radius Mean",
                    6.9, 28.2, 14.12,
                    step=0.01
                )

                texture_mean = st.number_input(
                    "Texture Mean",
                    9.7, 39.3, 19.29,
                    step=0.01
                )

                perimeter_mean = st.number_input(
                    "Perimeter Mean",
                    43.7, 188.5, 91.96,
                    step=0.01
                )

                area_mean = st.number_input(
                    "Area Mean",
                    143.5, 2501.0, 654.8,
                    step=0.1
                )

                smoothness_mean = st.number_input(
                    "Smoothness Mean",
                    0.05, 0.17, 0.096,
                    step=0.001,
                    format="%.4f"
                )


            with col2:

                compactness_mean = st.number_input(
                    "Compactness Mean",
                    0.01, 0.35, 0.104,
                    step=0.001,
                    format="%.4f"
                )


                concavity_mean = st.number_input(
                    "Concavity Mean",
                    0.0, 0.43, 0.088,
                    step=0.001,
                    format="%.4f"
                )


                concave_points_mean = st.number_input(
                    "Concave Points Mean",
                    0.0, 0.21, 0.048,
                    step=0.001,
                    format="%.4f"
                )


                symmetry_mean = st.number_input(
                    "Symmetry Mean",
                    0.10, 0.31, 0.181,
                    step=0.001,
                    format="%.4f"
                )


                fractal_dimension_mean = st.number_input(
                    "Fractal Dimension Mean",
                    0.04, 0.10, 0.062,
                    step=0.001,
                    format="%.4f"
                )



# ==================================================
# TAB 2 : STANDARD ERROR
# ==================================================

    with tab2:

        with st.container(border=True):

            col1, col2 = st.columns(2)


            with col1:

                radius_se = st.number_input(
                    "Radius SE",
                    0.1, 3.0, 0.405
                )

import textwrap

import streamlit as st
import pandas as pd

from utils.loader import load_model
from utils.risk import get_risk_level, create_risk_gauge
from utils.ai_summary import render_ai_summary_section


# ==================================================
# MODEL
# ==================================================

@st.cache_resource
def get_breast_model():
    return load_model("models/breast_logistic.pkl")


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
            margin:5px 0px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# CARD
# ==================================================

def render_card(title, content):
    """
    IMPORTANT: build the HTML as a single line with no leading
    whitespace on any line. Streamlit's markdown renderer treats
    lines indented 4+ spaces as a Markdown code block, which makes
    the HTML show up as literal text instead of being rendered —
    that was the bug here.
    """

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

    items = [
        ("Age", general_data.get("age", "-")),
        ("BMI", general_data.get("bmi", "-")),
        ("Smoking Status", general_data.get("smoking_status", "-")),
        ("Physical Activity", general_data.get("physical_activity", "-")),
    ]

    for col, (label, value) in zip([col1, col2, col3, col4], items):

        with col:

            card_html = (
                f'<div class="summary-card"><h4>{label}</h4><p>{value}</p></div>'
            )

            st.markdown(card_html, unsafe_allow_html=True)

    st.write("")


# ==================================================
# MAIN PAGE
# ==================================================

def breast_cancer_page(general_data):

    breast_model = get_breast_model()

    apply_medical_theme()
    apply_assessment_theme()

    if st.button("⬅️ Back to Assessment"):
        st.session_state.page = "assessment"
        st.rerun()

    st.markdown(
        '<div class="title">🎗 Breast Cancer Risk Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Smart breast cancer risk evaluation based on tumor measurements.</div>',
        unsafe_allow_html=True
    )

    render_health_summary(general_data)

    st.divider()

    st.subheader("🎗 Breast Cancer Measurements")

    tab1, tab2, tab3 = st.tabs([
        "📏 Mean Features",
        "📊 Standard Error",
        "⚠️ Worst Features"
    ])

    # ==================================================
    # TAB 1 : MEAN FEATURES
    # ==================================================

    with tab1:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                radius_mean = st.number_input("Radius Mean", 6.9, 28.2, 14.12, step=0.01)
                texture_mean = st.number_input("Texture Mean", 9.7, 39.3, 19.29, step=0.01)
                perimeter_mean = st.number_input("Perimeter Mean", 43.7, 188.5, 91.96, step=0.01)
                area_mean = st.number_input("Area Mean", 143.5, 2501.0, 654.8, step=0.1)
                smoothness_mean = st.number_input("Smoothness Mean", 0.05, 0.17, 0.096, step=0.001, format="%.4f")

            with col2:

                compactness_mean = st.number_input("Compactness Mean", 0.01, 0.35, 0.104, step=0.001, format="%.4f")
                concavity_mean = st.number_input("Concavity Mean", 0.0, 0.43, 0.088, step=0.001, format="%.4f")
                concave_points_mean = st.number_input("Concave Points Mean", 0.0, 0.21, 0.048, step=0.001, format="%.4f")
                symmetry_mean = st.number_input("Symmetry Mean", 0.10, 0.31, 0.181, step=0.001, format="%.4f")
                fractal_dimension_mean = st.number_input("Fractal Dimension Mean", 0.04, 0.10, 0.062, step=0.001, format="%.4f")

    # ==================================================
    # TAB 2 : STANDARD ERROR
    # ==================================================

    with tab2:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                radius_se = st.number_input("Radius SE", 0.1, 3.0, 0.405)
                texture_se = st.number_input("Texture SE", 0.3, 5.0, 1.216)
                perimeter_se = st.number_input("Perimeter SE", 0.7, 22.0, 2.866)
                area_se = st.number_input("Area SE", 6.0, 550.0, 40.3)
                smoothness_se = st.number_input("Smoothness SE", 0.001, 0.04, 0.007, format="%.4f")

            with col2:

                compactness_se = st.number_input("Compactness SE", 0.002, 0.14, 0.025, format="%.4f")
                concavity_se = st.number_input("Concavity SE", 0.0, 0.4, 0.031, format="%.4f")
                concave_points_se = st.number_input("Concave Points SE", 0.0, 0.06, 0.011, format="%.4f")
                symmetry_se = st.number_input("Symmetry SE", 0.007, 0.08, 0.020, format="%.4f")
                fractal_dimension_se = st.number_input("Fractal Dimension SE", 0.0008, 0.03, 0.003, format="%.4f")

    # ==================================================
    # TAB 3 : WORST FEATURES
    # ==================================================

    with tab3:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                radius_worst = st.number_input("Radius Worst", 7.9, 36.0, 16.27, step=0.01)
                texture_worst = st.number_input("Texture Worst", 12.0, 50.0, 25.38, step=0.01)
                perimeter_worst = st.number_input("Perimeter Worst", 50.0, 251.0, 107.5, step=0.1)
                area_worst = st.number_input("Area Worst", 180.0, 4254.0, 880.0, step=0.1)
                smoothness_worst = st.number_input("Smoothness Worst", 0.07, 0.22, 0.13, format="%.4f")

            with col2:

                compactness_worst = st.number_input("Compactness Worst", 0.02, 1.0, 0.25, format="%.4f")
                concavity_worst = st.number_input("Concavity Worst", 0.0, 1.2, 0.27, format="%.4f")
                concave_points_worst = st.number_input("Concave Points Worst", 0.0, 0.3, 0.11, format="%.4f")
                symmetry_worst = st.number_input("Symmetry Worst", 0.15, 0.7, 0.29, format="%.4f")
                fractal_dimension_worst = st.number_input("Fractal Dimension Worst", 0.05, 0.2, 0.08, format="%.4f")

        st.write("")

    if st.button("🔍 Analyze Breast Cancer Risk", use_container_width=True):

        data = pd.DataFrame({
            "radius_mean": [radius_mean],
            "texture_mean": [texture_mean],
            "perimeter_mean": [perimeter_mean],
            "area_mean": [area_mean],
            "smoothness_mean": [smoothness_mean],
            "compactness_mean": [compactness_mean],
            "concavity_mean": [concavity_mean],
            "concave points_mean": [concave_points_mean],
            "symmetry_mean": [symmetry_mean],
            "fractal_dimension_mean": [fractal_dimension_mean],
            "radius_se": [radius_se],
            "texture_se": [texture_se],
            "perimeter_se": [perimeter_se],
            "area_se": [area_se],
            "smoothness_se": [smoothness_se],
            "compactness_se": [compactness_se],
            "concavity_se": [concavity_se],
            "concave points_se": [concave_points_se],
            "symmetry_se": [symmetry_se],
            "fractal_dimension_se": [fractal_dimension_se],
            "radius_worst": [radius_worst],
            "texture_worst": [texture_worst],
            "perimeter_worst": [perimeter_worst],
            "area_worst": [area_worst],
            "smoothness_worst": [smoothness_worst],
            "compactness_worst": [compactness_worst],
            "concavity_worst": [concavity_worst],
            "concave points_worst": [concave_points_worst],
            "symmetry_worst": [symmetry_worst],
            "fractal_dimension_worst": [fractal_dimension_worst]
        })

        probability = breast_model.predict_proba(data)[0][1]
        prediction = breast_model.predict(data)[0]

        risk_level, message = get_risk_level(probability, "Breast Cancer")

        patient_data = {
            "Age": general_data["age"],
            "BMI": general_data["bmi"],
            "Radius Mean": radius_mean,
            "Texture Mean": texture_mean,
            "Area Mean": area_mean,
            "Radius Worst": radius_worst,
            "Texture Worst": texture_worst,
            "Area Worst": area_worst,
            "Concavity Worst": concavity_worst,
            "Concave Points Worst": concave_points_worst
        }

        st.session_state["breast_result"] = {
            "probability": probability,
            "risk_level": risk_level,
            "message": message,
            "prediction": prediction,
            "patient_data": patient_data
        }

        # Clear old AI summaries tied to older inputs
        st.session_state.pop("breast_ai_summary_en", None)
        st.session_state.pop("breast_ai_summary_ar", None)
        st.session_state.pop("breast_ai_summary_lang", None)

    # ==================================================
    # DISPLAY RESULT
    # ==================================================

    if "breast_result" in st.session_state:

        result = st.session_state["breast_result"]

        st.subheader("📊 Prediction Result")

        create_risk_gauge(result["probability"], "Breast Cancer")
        st.info(result["message"])

        # ==============================
        # Final Prediction Card
        # ==============================

        if "High" in result["risk_level"] or "Moderate" in result["risk_level"]:

            render_card(
                "Final Result",
                """
                <div style="text-align:center;">
                <h2 style="color:#dc2626;">🔴 Increased Breast Cancer Risk Pattern Detected</h2>
                <p>The model detected patterns associated with increased breast cancer risk. Please consult a healthcare professional for further evaluation.</p>
                </div>
                """
            )

        else:

            render_card(
                "Final Result",
                """
                <div style="text-align:center;">
                <h2 style="color:#16a34a;">🟢 Low Breast Cancer Risk Pattern Detected</h2>
                <p>The model did not detect strong patterns associated with breast cancer.</p>
                </div>
                """
            )

        # ==============================
        # AI Summary
        # ==============================

        render_ai_summary_section(
            page_key="breast",
            disease_label="Breast Cancer",
            patient_data=result["patient_data"],
            probability=result["probability"],
            risk_level=result["risk_level"]
        )
