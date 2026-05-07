"""
🔥 Calorie Burnt Prediction — Main App
Run with: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="CalorieAI — Burn Predictor",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3, .big-title {
    font-family: 'Syne', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f0f 0%, #1a1a2e 100%);
    border-right: 1px solid #ff4d1c33;
}
[data-testid="stSidebar"] * {
    color: #f0ede8 !important;
}

/* Main background */
.stApp {
    background: #0d0d0d;
    color: #f0ede8;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a1a1a, #222);
    border: 1px solid #ff4d1c44;
    border-radius: 12px;
    padding: 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ff4d1c, #ff8c42) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px #ff4d1c55 !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px #ff4d1c88 !important;
}

/* Sliders accent */
[data-testid="stSlider"] > div > div > div > div {
    background: #ff4d1c !important;
}

/* Input fields */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #f0ede8 !important;
    border-radius: 8px !important;
}

/* Success / Info boxes */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}

.block-container {
    padding-top: 2rem !important;
}

.nav-pill {
    display: inline-block;
    background: #ff4d1c22;
    border: 1px solid #ff4d1c55;
    color: #ff8c42;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.5rem 0 1rem;'>
        <div style='font-size:2.5rem;'>🔥</div>
        <div style='font-family:Syne,sans-serif; font-size:1.3rem;
                    font-weight:800; color:#ff8c42; letter-spacing:0.05em;'>
            CalorieAI
        </div>
        <div style='font-size:0.75rem; color:#888; margin-top:4px;'>
            Burn Prediction Engine
        </div>
    </div>
    <hr style='border-color:#ff4d1c22; margin: 0.5rem 0 1.2rem;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠  Home & Predict", "📊  EDA & Insights",
         "🤖  Model Comparison", "📜  Workout History",
         "📄  Export Report"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style='border-color:#ff4d1c22; margin: 1.5rem 0 0.8rem;'>
    <div style='font-size:0.7rem; color:#555; text-align:center;'>
        Final Year Major Project<br>
        <span style='color:#ff4d1c88;'>ML · XGBoost · Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Page Router ──────────────────────────────────────────────────────────────
if "🏠" in page:
    from pages.predict import show
    show()
elif "📊" in page:
    from pages.eda import show
    show()
elif "🤖" in page:
    from pages.model_comparison import show
    show()
elif "📜" in page:
    from pages.history import show
    show()
elif "📄" in page:
    from pages.report import show
    show()
