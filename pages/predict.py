"""
🏠 Home & Predict Page
"""
import streamlit as st
import numpy as np
import joblib
import json
from datetime import datetime

def show():
    # Load model
    try:
        model  = joblib.load("model.pkl")
        scaler = joblib.load("scaler.pkl")
        with open("model_meta.json") as f:
            meta = json.load(f)
        model_loaded = True
    except:
        model_loaded = False

    # Header
    st.markdown("""
    <div style='margin-bottom:0.5rem;'>
        <span class='nav-pill'>🔥 Predictor</span>
    </div>
    <h1 style='font-family:Syne,sans-serif; font-size:2.6rem;
               font-weight:800; color:#f0ede8; margin:0; line-height:1.1;'>
        How Many Calories<br>
        <span style='color:#ff4d1c;'>Will You Burn?</span>
    </h1>
    <p style='color:#888; margin-top:0.6rem; font-size:1rem;'>
        Enter your stats below — our XGBoost model predicts your calorie burn
        with <strong style='color:#ff8c42;'>99.77% accuracy (R²)</strong>.
    </p>
    """, unsafe_allow_html=True)

    if not model_loaded:
        st.error("⚠️ Model not found. Please run `python model_training.py` first.")
        return

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Input Form ────────────────────────────────────────────────────────────
    col_l, col_r = st.columns([1.1, 0.9], gap="large")

    with col_l:
        st.markdown("#### 👤 Personal Details")
        c1, c2 = st.columns(2)
        with c1:
            gender   = st.selectbox("Gender", ["Male", "Female"])
            age      = st.slider("Age (years)", 10, 80, 25)
        with c2:
            height   = st.number_input("Height (cm)", 100.0, 220.0, 170.0, step=0.5)
            weight   = st.number_input("Weight (kg)", 30.0, 150.0, 70.0, step=0.5)

        st.markdown("#### 🏃 Exercise Details")
        c3, c4 = st.columns(2)
        with c3:
            duration   = st.slider("Duration (min)", 1, 120, 30)
            heart_rate = st.slider("Heart Rate (bpm)", 60, 200, 110)
        with c4:
            body_temp  = st.slider("Body Temp (°C)", 36.0, 42.0, 38.5, step=0.1)
            exercise_type = st.selectbox("Exercise Type",
                ["Running", "Cycling", "Swimming", "HIIT", "Yoga", "Weight Training"])

        # Derived
        bmi          = weight / ((height / 100) ** 2)
        effort_index = heart_rate * duration
        gender_val   = 0 if gender == "Male" else 1

        # BMI display
        bmi_cat = ("Underweight" if bmi < 18.5 else
                   "Normal"      if bmi < 25   else
                   "Overweight"  if bmi < 30   else "Obese")
        bmi_col = ("#4ecdc4" if bmi_cat == "Normal" else
                   "#ffe66d" if bmi_cat in ["Underweight", "Overweight"] else "#ff4d1c")

        st.markdown(f"""
        <div style='background:#1a1a1a; border:1px solid #333; border-radius:10px;
                    padding:0.8rem 1rem; margin-top:0.5rem; display:flex;
                    justify-content:space-between; align-items:center;'>
            <span style='color:#888; font-size:0.85rem;'>Calculated BMI</span>
            <span style='font-family:Syne,sans-serif; font-weight:700;
                         font-size:1.1rem; color:{bmi_col};'>
                {bmi:.1f} — {bmi_cat}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("🔥 Predict Calories Burnt", use_container_width=True)

    # ─── Results Panel ─────────────────────────────────────────────────────────
    with col_r:
        st.markdown("#### 📈 Your Prediction")

        if predict_btn:
            features = np.array([[
                gender_val, age, height, weight,
                duration, heart_rate, body_temp,
                bmi, effort_index
            ]])
            features_scaled = scaler.transform(features)
            calories = model.predict(features_scaled)[0]
            calories = max(0, round(calories, 1))

            # Store in session history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "time":          datetime.now().strftime("%H:%M:%S"),
                "date":          datetime.now().strftime("%Y-%m-%d"),
                "gender":        gender,
                "age":           age,
                "weight":        weight,
                "height":        height,
                "duration":      duration,
                "heart_rate":    heart_rate,
                "body_temp":     body_temp,
                "exercise_type": exercise_type,
                "bmi":           round(bmi, 1),
                "calories":      calories
            })

            # Intensity classification
            cal_per_min = calories / duration
            if cal_per_min < 5:
                intensity, icon, color = "Light", "🟢", "#4ecdc4"
            elif cal_per_min < 9:
                intensity, icon, color = "Moderate", "🟡", "#ffe66d"
            elif cal_per_min < 13:
                intensity, icon, color = "High", "🟠", "#ff8c42"
            else:
                intensity, icon, color = "Peak", "🔴", "#ff4d1c"

            # Big calorie display
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#1a1a1a,#111);
                        border:2px solid {color}44; border-radius:16px;
                        padding:2rem; text-align:center; margin-bottom:1rem;'>
                <div style='font-size:0.8rem; color:#888; text-transform:uppercase;
                            letter-spacing:0.1em; font-family:Syne,sans-serif;'>
                    Predicted Calories Burnt
                </div>
                <div style='font-family:Syne,sans-serif; font-size:4rem;
                            font-weight:800; color:{color}; line-height:1.1;
                            margin:0.5rem 0;'>
                    {calories:,.1f}
                </div>
                <div style='font-size:0.9rem; color:#888;'>kcal</div>
                <hr style='border-color:#333; margin:1rem 0;'>
                <div style='color:{color}; font-family:Syne,sans-serif;
                            font-weight:700; font-size:1.1rem;'>
                    {icon} {intensity} Intensity
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Stats grid
            col_a, col_b = st.columns(2)
            col_a.metric("⏱ Cal / Minute", f"{cal_per_min:.1f} kcal")
            col_b.metric("💪 Effort Index", f"{effort_index:,}")

            # Equivalent foods
            st.markdown("#### 🍔 That's equivalent to burning off:")
            foods = [
                ("🍫", "Chocolate Bar", 230),
                ("🍕", "Pizza Slice",   285),
                ("🍔", "Burger",        550),
                ("🥤", "Soda Can",      150),
                ("🍚", "Bowl of Rice",  200),
            ]
            food_html = ""
            for emoji, name, kcal in foods:
                count = calories / kcal
                food_html += f"""
                <div style='display:flex; justify-content:space-between;
                            padding:0.4rem 0.6rem; border-bottom:1px solid #222;
                            font-size:0.85rem;'>
                    <span>{emoji} {name}</span>
                    <span style='color:#ff8c42; font-weight:600;'>× {count:.1f}</span>
                </div>"""
            st.markdown(f"""
            <div style='background:#111; border:1px solid #333;
                        border-radius:10px; overflow:hidden;'>{food_html}</div>
            """, unsafe_allow_html=True)

            # Tip
            st.markdown("<br>", unsafe_allow_html=True)
            tips = {
                "Light":    "💡 Increase heart rate or duration to burn more.",
                "Moderate": "💪 Good steady pace — consistency is key!",
                "High":     "🔥 Great intensity! Stay hydrated.",
                "Peak":     "🏆 Elite effort! Ensure proper recovery."
            }
            st.info(tips[intensity])

        else:
            st.markdown("""
            <div style='background:#111; border:2px dashed #333;
                        border-radius:16px; padding:3rem 2rem;
                        text-align:center; color:#555;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>🎯</div>
                <div style='font-family:Syne,sans-serif; font-size:1rem;'>
                    Fill in your details and hit<br>
                    <strong style='color:#ff4d1c;'>Predict Calories Burnt</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Model stats preview
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🏆 Model Performance")
            m = meta["model_results"]["XGBoost"]
            c1, c2, c3 = st.columns(3)
            c1.metric("R² Score", f"{m['R2']:.4f}")
            c2.metric("MAE", f"{m['MAE']:.2f} kcal")
            c3.metric("RMSE", f"{m['RMSE']:.2f} kcal")
