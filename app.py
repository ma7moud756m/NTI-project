import streamlit as st

from screans.home import home_page
from screans.assessment import assessment_page
from disease_pages.stroke import stroke_page
from disease_pages.diabetes import diabetes_page
from disease_pages.heart import heart_page_test
from disease_pages.kidney import kidney_page
from disease_pages.breast_cancer import breast_cancer_page


st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_global_theme():
    """Shared visual system for every Streamlit screen."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

        :root { --ink:#102A43; --muted:#627D98; --brand:#087E8B; --brand-dark:#045C66;
                --soft:#F4FAFA; --line:#DCEBED; --surface:#FFFFFF; }
        html, body, [class*="css"] { font-family:'DM Sans', sans-serif; }
        .stApp { background:linear-gradient(135deg,#F6FBFC 0%,#FFFFFF 48%,#F2F9F9 100%); color:var(--ink); }
        .block-container { max-width:1240px; padding-top:2.1rem; padding-bottom:3rem; }
        h1, h2, h3 { font-family:'Manrope', sans-serif; color:var(--ink); letter-spacing:-.025em; }
        [data-testid="stSidebar"] { background:#073B4C; border-right:0; }
        [data-testid="stSidebar"] * { color:#E8F5F6; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#BFD7DC; }
        [data-testid="stSidebar"] .stButton > button { background:transparent; color:#E8F5F6; border:1px solid rgba(255,255,255,.16); box-shadow:none; text-align:left; }
        [data-testid="stSidebar"] .stButton > button:hover { background:rgba(255,255,255,.12); border-color:rgba(255,255,255,.34); color:#FFFFFF; }
        .stButton > button { min-height:44px; border-radius:10px; border:1px solid #087E8B; background:#087E8B; color:#fff; font-family:'DM Sans',sans-serif; font-weight:700; transition:all .18s ease; }
        .stButton > button:hover { background:#045C66; border-color:#045C66; transform:translateY(-1px); box-shadow:0 7px 15px rgba(8,126,139,.18); color:#fff; }
        .stDownloadButton > button { min-height:44px; border-radius:10px; font-weight:700; border-color:#087E8B; color:#087E8B; }
        [data-baseweb="input"] > div, [data-baseweb="select"] > div { border-radius:10px!important; border-color:#C7DDE0!important; background:#fff!important; }
        [data-baseweb="input"] > div:focus-within, [data-baseweb="select"] > div:focus-within { border-color:#087E8B!important; box-shadow:0 0 0 3px rgba(8,126,139,.12)!important; }
        [data-testid="stVerticalBlockBorderWrapper"] { background:#fff; border:1px solid var(--line); border-radius:16px; box-shadow:0 6px 18px rgba(16,42,67,.04); }
        [data-testid="stTabs"] button { font-weight:700; color:#627D98; }
        [data-testid="stTabs"] button[aria-selected="true"] { color:#087E8B; }
        [data-testid="stMetric"] { background:#fff; border:1px solid var(--line); padding:14px 16px; border-radius:14px; }
        [data-testid="stAlert"] { border-radius:12px; }
        hr { border-color:#DCEBED; margin:2rem 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_global_theme()

if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = None
if "general_data" not in st.session_state:
    st.session_state.general_data = None

st.sidebar.markdown("## 🩺 AI Health Assistant")
st.sidebar.markdown("Your health awareness companion")
st.sidebar.divider()

if st.sidebar.button("Overview", width="stretch"):
    st.session_state.page = "home"
    st.rerun()
if st.sidebar.button("Start assessment", width="stretch"):
    st.session_state.page = "assessment"
    st.rerun()

st.sidebar.markdown("<br><small>For awareness only — not a medical diagnosis.</small>", unsafe_allow_html=True)

if st.session_state.selected_disease:
    st.sidebar.divider()
    st.sidebar.caption("CURRENT ASSESSMENT")
    st.sidebar.success(st.session_state.selected_disease.replace("_", " "))

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "assessment":
    assessment_page()
elif st.session_state.page == "disease":
    pages = {
        "Stroke": stroke_page,
        "Diabetes": diabetes_page,
        "Heart Disease": heart_page_test,
        "Kidney Disease": kidney_page,
        "Breast_Cancer Disease": breast_cancer_page,
    }
    page = pages.get(st.session_state.selected_disease)
    if page:
        page(st.session_state.general_data)
    else:
        st.warning("Please choose a health assessment first.")
