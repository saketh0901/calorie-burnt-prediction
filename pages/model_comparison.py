"""
🤖 Model Comparison Page
"""
import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

COLORS = {"fire":"#ff4d1c","amber":"#ff8c42","teal":"#4ecdc4",
          "gold":"#ffe66d","bg":"#111111"}
TEMPLATE = dict(layout=dict(paper_bgcolor=COLORS["bg"],
    plot_bgcolor=COLORS["bg"], font=dict(color="#f0ede8", family="DM Sans")))

def show():
    try:
        with open("model_meta.json") as f:
            meta = json.load(f)
    except:
        st.error("Run model_training.py first.")
        return

    st.markdown("""
    <span class='nav-pill'>🤖 Models</span>
    <h1 style='font-family:Syne,sans-serif; font-size:2.4rem;
               font-weight:800; color:#f0ede8; margin:0.3rem 0;'>
        Model Performance<br>
        <span style='color:#ff4d1c;'>Head-to-Head</span>
    </h1>
    <p style='color:#888;'>Three algorithms benchmarked on the same test set.</p>
    """, unsafe_allow_html=True)

    results = meta["model_results"]
    models  = list(results.keys())
    best    = meta["best_model"]

    # ── Leaderboard ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    medal = {"XGBoost": "🥇", "Random Forest": "🥈", "Linear Regression": "🥉"}

    for name in sorted(models, key=lambda k: -results[k]["R2"]):
        m = results[name]
        is_best = name == best
        border  = "#ff4d1c" if is_best else "#2a2a2a"
        st.markdown(f"""
        <div style='background:#1a1a1a; border:1px solid {border};
                    border-radius:12px; padding:1.1rem 1.4rem;
                    display:flex; justify-content:space-between;
                    align-items:center; margin-bottom:0.7rem;'>
            <div>
                <span style='font-family:Syne,sans-serif; font-weight:700;
                             font-size:1.05rem; color:#f0ede8;'>
                    {medal.get(name,"▪")} {name}
                </span>
                {"<span style='background:#ff4d1c22;color:#ff8c42;font-size:0.7rem;" +
                  "border-radius:10px;padding:2px 8px;margin-left:8px;" +
                  "font-family:Syne,sans-serif;font-weight:600;'>" +
                  "BEST MODEL</span>" if is_best else ""}
            </div>
            <div style='display:flex; gap:2rem;'>
                <div style='text-align:center;'>
                    <div style='font-size:0.72rem; color:#666;'>R² SCORE</div>
                    <div style='font-family:Syne,sans-serif; font-weight:700;
                                font-size:1.1rem; color:#4ecdc4;'>{m['R2']:.4f}</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:0.72rem; color:#666;'>MAE</div>
                    <div style='font-family:Syne,sans-serif; font-weight:700;
                                font-size:1.1rem; color:#ffe66d;'>{m['MAE']:.2f}</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:0.72rem; color:#666;'>RMSE</div>
                    <div style='font-family:Syne,sans-serif; font-weight:700;
                                font-size:1.1rem; color:#ff8c42;'>{m['RMSE']:.2f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Charts ─────────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 R² Score Comparison")
        fig = go.Figure(go.Bar(
            x=models,
            y=[results[m]["R2"] for m in models],
            marker=dict(
                color=[COLORS["fire"] if m == best else COLORS["teal"] for m in models],
                line=dict(color="#333", width=1)
            ),
            text=[f"{results[m]['R2']:.4f}" for m in models],
            textposition="outside"
        ))
        fig.update_layout(
            height=300, margin=dict(t=30,b=10,l=10,r=10),
            yaxis=dict(range=[0.95, 1.002], gridcolor="#222"),
            xaxis=dict(gridcolor="#222"),
            paper_bgcolor=COLORS["bg"], plot_bgcolor=COLORS["bg"],
            font=dict(color="#f0ede8")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📉 MAE & RMSE Comparison")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="MAE", x=models,
            y=[results[m]["MAE"] for m in models],
            marker_color=COLORS["fire"]
        ))
        fig2.add_trace(go.Bar(
            name="RMSE", x=models,
            y=[results[m]["RMSE"] for m in models],
            marker_color=COLORS["teal"]
        ))
        fig2.update_layout(
            barmode="group", height=300, margin=dict(t=30,b=10,l=10,r=10),
            paper_bgcolor=COLORS["bg"], plot_bgcolor=COLORS["bg"],
            font=dict(color="#f0ede8"),
            yaxis=dict(gridcolor="#222"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Feature Importance ─────────────────────────────────────────────────────
    if meta.get("feature_importance"):
        st.markdown("#### 🧬 Feature Importance (XGBoost)")
        fi = meta["feature_importance"]
        fi_sorted = dict(sorted(fi.items(), key=lambda x: x[1]))

        readable = {
            "Gender":"Gender","Age":"Age","Height":"Height","Weight":"Weight",
            "Duration":"Duration","Heart_Rate":"Heart Rate","Body_Temp":"Body Temp",
            "BMI":"BMI","Effort_Index":"Effort Index"
        }
        labels = [readable.get(k, k) for k in fi_sorted]
        values = list(fi_sorted.values())

        fig3 = go.Figure(go.Bar(
            x=values, y=labels, orientation="h",
            marker=dict(
                color=values,
                colorscale=[[0,"#1a1a1a"],[0.5,"#ff8c42"],[1,"#ff4d1c"]],
                line=dict(color="#333", width=0.5)
            ),
            text=[f"{v:.3f}" for v in values],
            textposition="outside"
        ))
        fig3.update_layout(
            height=340, margin=dict(t=10,b=10,l=10,r=60),
            paper_bgcolor=COLORS["bg"], plot_bgcolor=COLORS["bg"],
            font=dict(color="#f0ede8"),
            xaxis=dict(gridcolor="#222")
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── Why XGBoost Wins ────────────────────────────────────────────────────────
    st.markdown("#### 💡 Why XGBoost Outperforms")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**Gradient Boosting**\nBuilds trees sequentially, each correcting previous errors.")
    with col_b:
        st.info("**Regularization**\nL1/L2 penalties prevent overfitting on small features.")
    with col_c:
        st.info("**Non-linearity**\nCaptures complex relationships linear models miss.")
