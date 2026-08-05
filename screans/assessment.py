import streamlit as st


DISEASES = [
    ("Stroke", "🧠", "Assess stroke-related risk factors"),
    ("Diabetes", "🩸", "Review metabolic health indicators"),
    ("Heart Disease", "♥", "Explore cardiovascular risk"),
    ("Kidney Disease", "◒", "Review kidney-health indicators"),
    ("Breast_Cancer Disease", "🎗", "Assess tumour measurement patterns"),
]


def assessment_page():
    st.markdown(
        """
        <style>
        .page-head { padding:8px 0 26px; }.page-head h1 { font-size:2.35rem; margin:0 0 7px; }.page-head p { color:#627D98; margin:0; font-size:1.02rem; }
        .step { display:inline-flex; align-items:center; gap:8px; background:#E8F6F7; color:#07616B; padding:7px 11px; border-radius:999px; font-size:.78rem; font-weight:700; margin-bottom:16px; }
        .form-title { font-size:1.18rem; font-weight:800; margin:0 0 4px; color:#102A43; }.form-help { color:#627D98; font-size:.9rem; margin-bottom:16px; }
        .choice-card { background:#fff; border:1px solid #DCEBED; border-radius:16px; padding:20px; min-height:154px; box-shadow:0 6px 18px rgba(16,42,67,.035); }.choice-icon { color:#087E8B; font-size:1.7rem; margin-bottom:12px; }.choice-card h3 { font-size:1.02rem; margin:0 0 6px; }.choice-card p { color:#627D98; margin:0 0 14px; font-size:.89rem; min-height:40px; }
        </style>
        <div class="page-head"><div class="step">STEP 1 OF 2 · YOUR HEALTH PROFILE</div><h1>Start your health assessment</h1><p>Complete a short general profile, then select the assessment you would like to run.</p></div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("← Back to overview", type="secondary"):
        st.session_state.page = "home"
        st.rerun()

    with st.container(border=True):
        st.markdown('<div class="form-title">General health information</div><div class="form-help">This profile is reused in the selected assessment.</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female"])
        with col2:
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
            weight = st.number_input("Weight (kg)", min_value=20, max_value=250, value=70)
        with col3:
            smoking_status = st.selectbox("Smoking status", ["never smoked", "formerly smoked", "smokes", "Unknown"])
            physical_activity = st.selectbox("Physical activity", ["Low", "Medium", "High"])
        family_history = st.selectbox("Family history of chronic disease", ["No", "Yes"], help="A close family member with a relevant long-term condition.")

    bmi = weight / ((height / 100) ** 2)
    bmi_col, guidance_col = st.columns([1, 2])
    with bmi_col:
        st.metric("Calculated BMI", f"{bmi:.1f}")
    with guidance_col:
        st.info("Your BMI is calculated from the height and weight entered above and is used only as one of several screening indicators.")

    st.session_state.general_data = {"age": age, "gender": gender, "bmi": bmi, "smoking_status": smoking_status, "physical_activity": physical_activity, "family_history": family_history}
    st.markdown('<div class="step">STEP 2 OF 2 · CHOOSE A MODEL</div><div class="form-title">What would you like to assess?</div><div class="form-help">Select one assessment to continue to its detailed health questions.</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for index, (name, icon, description) in enumerate(DISEASES):
        with cols[index % 3]:
            st.markdown(f'<div class="choice-card"><div class="choice-icon">{icon}</div><h3>{name.replace("_", " ")}</h3><p>{description}</p></div>', unsafe_allow_html=True)
            if st.button("Continue", key=f"choose_{name}", width="stretch"):
                st.session_state.selected_disease = name
                st.session_state.page = "disease"
                st.rerun()
