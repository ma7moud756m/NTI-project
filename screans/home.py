import streamlit as st


def home_page():
    st.markdown(
        """
        <style>
        .hero-card { background:linear-gradient(118deg,#073B4C 0%,#075B67 55%,#087E8B 100%); border-radius:24px; padding:48px 52px; color:white; box-shadow:0 18px 45px rgba(7,59,76,.18); overflow:hidden; position:relative; min-height:380px; display:flex; flex-direction:column; justify-content:center; }
        .hero-card:after { content:''; position:absolute; width:360px; height:360px; border:1px solid rgba(255,255,255,.14); border-radius:50%; right:-100px; top:-145px; box-shadow:0 0 0 42px rgba(255,255,255,.035),0 0 0 84px rgba(255,255,255,.025); }
        .eyebrow { color:#90E0E8; letter-spacing:.12em; font-size:.75rem; font-weight:700; text-transform:uppercase; margin-bottom:14px; }
        .hero-card h1 { color:#fff; font-size:clamp(2.15rem,4vw,3.5rem); max-width:620px; margin:0 0 16px; line-height:1.1; }
        .hero-card p { max-width:600px; margin:0; font-size:1.08rem; line-height:1.7; color:#D8F3F5; }
        .section-kicker { color:#087E8B; font-size:.78rem; letter-spacing:.1em; font-weight:700; text-transform:uppercase; margin-top:42px; }
        .section-heading { font-size:1.75rem; font-weight:800; margin:6px 0 20px; }
        .feature { background:#fff; border:1px solid #DCEBED; border-radius:16px; padding:24px; min-height:184px; box-shadow:0 6px 18px rgba(16,42,67,.04); }
        .feature-icon { font-size:1.65rem; width:46px; height:46px; display:grid; place-items:center; background:#E8F6F7; border-radius:12px; margin-bottom:15px; }
        .feature h3 { font-size:1.04rem; margin:0 0 8px; }.feature p { color:#627D98; line-height:1.6; margin:0; font-size:.94rem; }
        .model-item { background:#fff; border:1px solid #DCEBED; border-radius:14px; padding:16px; min-height:92px; }.model-item strong { display:block; color:#102A43; margin-bottom:4px; }.model-item span { color:#627D98; font-size:.83rem; }
        .notice { background:#FFF9EC; border-left:4px solid #E9A23B; padding:15px 18px; border-radius:10px; color:#5F4B20; font-size:.92rem; margin-top:30px; }
        [data-testid="stImage"] img { border-radius:24px; border:1px solid #DCEBED; box-shadow:0 18px 45px rgba(16,42,67,.12); }
        .trust-line { display:flex; gap:18px; flex-wrap:wrap; color:#C5E7E9; font-size:.78rem; margin-top:27px; }.trust-line span:before { content:'✓'; color:#90E0E8; font-weight:800; margin-right:6px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    hero_copy, hero_art = st.columns([1.35, 0.65], gap="large")
    with hero_copy:
        st.markdown(
            '''<div class="hero-card"><div class="eyebrow">AI-powered health awareness</div><h1>Understand your health indicators with more clarity.</h1><p>AI Health Assistant brings five screening models into one private, easy-to-follow assessment experience — with clear results and practical next steps.</p><div class="trust-line"><span>Private by design</span><span>Five health models</span><span>Arabic support</span></div></div>''',
            unsafe_allow_html=True,
        )
    with hero_art:
        st.image("assets/health_ai.png", use_container_width=True, output_format="PNG")

    st.write("")
    if st.button("Start a health assessment  →", type="primary", width="content"):
        st.session_state.page = "assessment"
        st.rerun()

    st.markdown('<div class="section-kicker">How it helps</div><div class="section-heading">Designed for clarity, not complexity.</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    features = [
        ("◌", "Personal risk screening", "Enter relevant health information and receive a clear estimated risk level."),
        ("⌁", "Plain-language summary", "Turn model output into an understandable overview and general wellness guidance."),
        ("◉", "Bilingual support", "Generate a report in English, then translate the health summary to Arabic when needed."),
    ]
    for col, (icon, title, text) in zip(cols, features):
        with col:
            st.markdown(f'<div class="feature"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">Available assessments</div><div class="section-heading">Five models. One streamlined experience.</div>', unsafe_allow_html=True)
    models = [("Heart disease", "Cardiovascular indicators"), ("Diabetes", "Lifestyle and lab indicators"), ("Chronic kidney disease", "Clinical health measurements"), ("Stroke", "Risk-factor screening"), ("Breast cancer", "Tumour measurement patterns")]
    model_cols = st.columns(5)
    for col, (title, desc) in zip(model_cols, models):
        with col:
            st.markdown(f'<div class="model-item"><strong>{title}</strong><span>{desc}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="notice"><strong>Important:</strong> This tool supports health awareness only. It does not provide a diagnosis or replace advice from a qualified healthcare professional.</div>', unsafe_allow_html=True)
