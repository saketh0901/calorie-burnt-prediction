"""
📄 Export Report Page
"""
import streamlit as st
import json
from fpdf import FPDF
from datetime import datetime
import io

def generate_pdf(meta, history):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_doc_option("core_fonts_encoding", "windows-1252") 

    # ── Title Page ─────────────────────────────────────────────────────────────
    pdf.set_fill_color(13, 13, 13)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(255, 77, 28)
    pdf.rect(0, 0, 210, 3, "F")

    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(240, 237, 232)
    pdf.ln(20)
    pdf.cell(0, 12, "CALORIE BURNT PREDICTION", align="C", ln=True)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(255, 140, 66)
    pdf.cell(0, 8, "Machine Learning Project Report", align="C", ln=True)
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(136, 136, 136)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", align="C", ln=True)
    pdf.ln(16)

    # Divider
    pdf.set_draw_color(255, 77, 28)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(12)

    def section(title):
        pdf.ln(8)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(255, 140, 66)
        pdf.cell(0, 7, title, ln=True)
        pdf.set_draw_color(255, 77, 28)
        pdf.set_line_width(0.3)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(4)

    def body(text):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(200, 197, 192)
        pdf.multi_cell(0, 5.5, text)

    # ── 1. Project Overview ────────────────────────────────────────────────────
    section("1. PROJECT OVERVIEW")
    body(
        "This project builds a machine learning model to predict the number of calories "
        "burnt during physical exercise. Using biometric and exercise features including "
        "gender, age, height, weight, duration, heart rate, and body temperature, three "
        "regression models were trained and evaluated: Linear Regression, Random Forest, "
        "and XGBoost. The best-performing model (XGBoost) was deployed as a Streamlit "
        "web application with real-time prediction capability."
    )

    # ── 2. Dataset ─────────────────────────────────────────────────────────────
    section("2. DATASET DESCRIPTION")
    body(
        f"Dataset: 15,000 exercise records with 9 features.\n"
        f"Training set: {meta['train_size']:,} records   |   "
        f"Test set: {meta['test_size']:,} records\n\n"
        "Features used:\n"
        "  - Gender (0=Male, 1=Female)\n"
        "  - Age, Height (cm), Weight (kg)\n"
        "  - Exercise Duration (minutes)\n"
        "  - Heart Rate (bpm), Body Temperature (°C)\n"
        "  - Derived: BMI, Effort Index (HR × Duration)\n\n"
        "Target: Calories burnt (continuous - regression problem)"
    )

    # ── 3. Model Results ───────────────────────────────────────────────────────
    section("3. MODEL PERFORMANCE COMPARISON")
    results = meta["model_results"]
    models  = sorted(results.items(), key=lambda x: -x[1]["R2"])

    for name, m in models:
        star = "  *** BEST MODEL ***" if name == meta["best_model"] else ""
        pdf.set_font("Courier", "B" if star else "", 10)
        pdf.set_text_color(255 if star else 200, 140 if star else 197, 66 if star else 192)
        pdf.cell(0, 6, f"  {name}{star}", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(160, 157, 152)
        pdf.cell(0, 5, f"     R²={m['R2']:.4f}   MAE={m['MAE']:.2f} kcal   RMSE={m['RMSE']:.2f} kcal", ln=True)
        pdf.ln(2)

    # ── 4. Feature Importance ─────────────────────────────────────────────────
    section("4. FEATURE IMPORTANCE (XGBoost)")
    fi = meta.get("feature_importance", {})
    if fi:
        sorted_fi = sorted(fi.items(), key=lambda x: -x[1])
        readable  = {
            "Effort_Index":"Effort Index","Duration":"Duration",
            "Heart_Rate":"Heart Rate","Body_Temp":"Body Temp",
            "Weight":"Weight","BMI":"BMI","Age":"Age",
            "Height":"Height","Gender":"Gender"
        }
        for feat, imp in sorted_fi:
            label    = readable.get(feat, feat)
            bar_len  = int(imp * 400)
            bar_str  = "█" * bar_len + "░" * (40 - bar_len)
            pdf.set_font("Courier", "", 9)
            pdf.set_text_color(180, 177, 172)
            pdf.cell(0, 5, f"  {label:<16} {bar_str}  {imp:.4f}", ln=True)

    # ── 5. Workout History ─────────────────────────────────────────────────────
    if history:
        section("5. LOGGED WORKOUT SESSIONS")
        pdf.set_font("Courier", "B", 8)
        pdf.set_text_color(255, 140, 66)
        headers = f"{'#':<4}{'Exercise':<18}{'Duration':>10}{'Heart Rate':>12}{'BMI':>8}{'Calories':>12}"
        pdf.cell(0, 5, headers, ln=True)
        pdf.set_font("Courier", "", 8)
        for i, h in enumerate(history, 1):
            pdf.set_text_color(180, 177, 172)
            row = (f"{i:<4}{h['exercise_type']:<18}"
                   f"{str(h['duration'])+' min':>10}"
                   f"{str(h['heart_rate'])+' bpm':>12}"
                   f"{str(h['bmi']):>8}"
                   f"{str(h['calories'])+' kcal':>12}")
            pdf.cell(0, 5, row, ln=True)

    # ── 6. Conclusion ──────────────────────────────────────────────────────────
    section("6. CONCLUSION")
    body(
        f"The XGBoost regressor achieved a near-perfect R2 score of "
        f"{results[meta['best_model']]['R2']:.4f} with a Mean Absolute Error of only "
        f"{results[meta['best_model']]['MAE']:.2f} kcal, demonstrating that calorie burn "
        "can be reliably predicted from biometric and workout data. The Effort Index "
        "(Heart Rate × Duration) emerged as the most important feature, confirming the "
        "physiological relationship between sustained cardiovascular stress and energy "
        "expenditure.\n\n"
        "Future work could include integrating real-time wearable sensor data, adding "
        "more exercise modalities, and personalizing predictions with longitudinal user data."
    )

    # Footer
    pdf.ln(10)
    pdf.set_draw_color(255, 77, 28)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(85, 85, 85)
    pdf.cell(0, 5, "Calorie Burnt Prediction | Final Year Major Project | Built with XGBoost + Streamlit", align="C", ln=True)

    return bytes(pdf.output())


def show():
    try:
        with open("model_meta.json") as f:
            meta = json.load(f)
    except:
        st.error("Run model_training.py first.")
        return

    history = st.session_state.get("history", [])

    st.markdown("""
    <span class='nav-pill'>📄 Report</span>
    <h1 style='font-family:Syne,sans-serif; font-size:2.4rem;
               font-weight:800; color:#f0ede8; margin:0.3rem 0;'>
        Export Project<br>
        <span style='color:#ff4d1c;'>Report</span>
    </h1>
    <p style='color:#888;'>Generate a professional PDF report of your ML project results.</p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Preview what's included
    st.markdown("#### 📋 Report Includes")
    items = [
        ("📌", "Project Overview & Objective"),
        ("📦", "Dataset Description (15,000 records, 9 features)"),
        ("🤖", "3-Model Performance Comparison (R², MAE, RMSE)"),
        ("🧬", "Feature Importance Analysis (XGBoost)"),
        ("📜", f"Workout Sessions Logged ({len(history)} sessions)" if history else "📜 Workout History (none logged yet)"),
        ("✅", "Conclusion & Future Scope"),
    ]
    for icon, text in items:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:0.8rem;
                    padding:0.5rem 0; border-bottom:1px solid #1a1a1a;
                    font-size:0.9rem; color:#ccc;'>
            <span style='font-size:1.1rem;'>{icon}</span> {text}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📄 Generate & Download PDF Report", use_container_width=True):
        with st.spinner("Generating your report..."):
            pdf_bytes = generate_pdf(meta, history)
        fname = f"CaloriePrediction_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        st.download_button(
            label="⬇️ Download Report PDF",
            data=pdf_bytes,
            file_name=fname,
            mime="application/pdf",
            use_container_width=True
        )
        st.success("✅ Report generated! Click the button above to download.")
