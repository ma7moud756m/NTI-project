import streamlit as st


def apply_assessment_theme():
    """Final styling layer for each disease-specific assessment page."""
    st.markdown(
        """
        <style>
        .title { color:#102A43!important; font-family:'Manrope',sans-serif!important; font-size:2.2rem!important; font-weight:800!important; letter-spacing:-.035em; text-align:left!important; margin:16px 0 5px!important; }
        .subtitle { color:#627D98!important; text-align:left!important; font-size:1rem!important; margin:0 0 25px!important; }
        .card { background:#FFFFFF!important; border:1px solid #DCEBED!important; border-radius:16px!important; padding:22px!important; box-shadow:0 6px 18px rgba(16,42,67,.04)!important; }
        .card h3 { color:#102A43!important; font-family:'Manrope',sans-serif!important; }
        .summary-card { background:#FFFFFF!important; border:1px solid #DCEBED!important; border-radius:14px!important; padding:14px!important; text-align:left!important; box-shadow:0 4px 12px rgba(16,42,67,.035)!important; }
        .summary-card h4 { color:#627D98!important; letter-spacing:.04em; text-transform:uppercase; font-size:.7rem!important; }
        .summary-card p { color:#102A43!important; font-family:'Manrope',sans-serif!important; font-size:1.05rem!important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
