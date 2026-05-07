"""
📜 Workout History Page
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

COLORS = {"fire":"#ff4d1c","amber":"#ff8c42","teal":"#4ecdc4",
          "gold":"#ffe66d","bg":"#111111"}

def show():
    st.markdown("""
    <span class='nav-pill'>📜 History</span>
    <h1 style='font-family:Syne,sans-serif; font-size:2.4rem;
               font-weight:800; color:#f0ede8; margin:0.3rem 0;'>
        Your Workout<br>
        <span style='color:#ff4d1c;'>History</span>
    </h1>
    <p style='color:#888;'>All sessions logged in this session.</p>
    """, unsafe_allow_html=True)

    history = st.session_state.get("history", [])

    if not history:
        st.markdown("""
        <div style='background:#111; border:2px dashed #2a2a2a;
                    border-radius:16px; padding:4rem; text-align:center; color:#555;
                    margin-top:2rem;'>
            <div style='font-size:3rem; margin-bottom:1rem;'>🏃</div>
            <div style='font-family:Syne,sans-serif;'>
                No workouts logged yet.<br>
                <span style='color:#ff4d1c;'>Go to Home & Predict</span> to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame(history)

    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏋️ Sessions",      len(df))
    col2.metric("🔥 Total Calories", f"{df['calories'].sum():.0f} kcal")
    col3.metric("📊 Avg Calories",   f"{df['calories'].mean():.0f} kcal")
    col4.metric("⏱ Total Duration",  f"{df['duration'].sum()} min")

    st.markdown("---")

    # Calories trend chart
    if len(df) > 1:
        st.markdown("#### 📈 Calories Per Session")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(df)+1)), y=df["calories"],
            mode="lines+markers",
            line=dict(color=COLORS["fire"], width=2.5),
            marker=dict(size=8, color=COLORS["amber"]),
            fill="tozeroy",
            fillcolor="rgba(255,77,28,0.13)",
            name="Calories"
        ))
        fig.update_layout(
            height=280, margin=dict(t=10,b=10,l=10,r=10),
            paper_bgcolor=COLORS["bg"], plot_bgcolor=COLORS["bg"],
            font=dict(color="#f0ede8"),
            xaxis=dict(title="Session #", gridcolor="#222"),
            yaxis=dict(title="Calories (kcal)", gridcolor="#222")
        )
        st.plotly_chart(fig, use_container_width=True)

    # History table
    st.markdown("#### 🗂 Session Log")
    display_df = df[["time","exercise_type","duration","heart_rate","body_temp","bmi","calories"]].copy()
    display_df.columns = ["Time","Exercise","Duration (min)","Heart Rate","Body Temp (°C)","BMI","Calories (kcal)"]
    st.dataframe(display_df, use_container_width=True)

    # Clear history
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑 Clear History"):
        st.session_state.history = []
        st.rerun()
