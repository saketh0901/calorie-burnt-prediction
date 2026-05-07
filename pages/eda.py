"""
📊 EDA & Insights Page
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@st.cache_data
def load_data():
    df_e = pd.read_csv("dataset/exercise.csv")
    df_c = pd.read_csv("dataset/calories.csv")
    df   = pd.merge(df_e, df_c, on="User_ID")
    df["BMI"] = df["Weight"] / ((df["Height"] / 100) ** 2)
    df["Effort_Index"] = df["Heart_Rate"] * df["Duration"]
    df["Gender_Label"] = df["Gender"].map({"male":"Male","female":"Female"})
    df["Intensity"] = pd.cut(df["Calories"]/df["Duration"],
        bins=[0,5,9,13,999],
        labels=["Light","Moderate","High","Peak"])
    return df

COLORS = {
    "fire":   "#ff4d1c",
    "amber":  "#ff8c42",
    "teal":   "#4ecdc4",
    "gold":   "#ffe66d",
    "bg":     "#111111",
    "card":   "#1a1a1a",
    "border": "#2a2a2a"
}

TEMPLATE = dict(
    layout=dict(
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor =COLORS["bg"],
        font=dict(color="#f0ede8", family="DM Sans"),
        colorway=[COLORS["fire"], COLORS["teal"], COLORS["gold"], COLORS["amber"]],
    )
)

def show():
    df = load_data()

    st.markdown("""
    <span class='nav-pill'>📊 EDA</span>
    <h1 style='font-family:Syne,sans-serif; font-size:2.4rem;
               font-weight:800; color:#f0ede8; margin:0.3rem 0;'>
        Data Exploration &<br>
        <span style='color:#ff4d1c;'>Deep Insights</span>
    </h1>
    <p style='color:#888;'>15,000 workout records analysed across 9 features.</p>
    """, unsafe_allow_html=True)

    # ── Summary Cards ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📦 Records",    f"{len(df):,}")
    c2.metric("🔥 Avg Calories", f"{df['Calories'].mean():.0f} kcal")
    c3.metric("⏱ Avg Duration", f"{df['Duration'].mean():.0f} min")
    c4.metric("💓 Avg HR",      f"{df['Heart_Rate'].mean():.0f} bpm")
    c5.metric("🌡 Avg Temp",    f"{df['Body_Temp'].mean():.1f} °C")

    st.markdown("---")

    # ── Row 1: Distribution + Gender Split ────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔥 Calorie Distribution")
        fig = px.histogram(
            df, x="Calories", nbins=60,
            color_discrete_sequence=[COLORS["fire"]],
            template=TEMPLATE
        )
        fig.update_layout(
            height=300, margin=dict(t=10,b=10,l=10,r=10),
            bargap=0.05, xaxis_title="Calories (kcal)", yaxis_title="Count"
        )
        fig.update_traces(marker_line_color=COLORS["amber"], marker_line_width=0.5)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 👥 Gender Distribution")
        gender_counts = df["Gender_Label"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=gender_counts.index,
            values=gender_counts.values,
            hole=0.55,
            marker=dict(colors=[COLORS["fire"], COLORS["teal"]],
                        line=dict(color=COLORS["bg"], width=3))
        ))
        fig2.update_layout(
            height=300, margin=dict(t=10,b=10,l=10,r=10),
            paper_bgcolor=COLORS["bg"],
            font=dict(color="#f0ede8"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Row 2: Calories vs Duration + Correlation ─────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### ⏱ Calories vs Duration")
        sample = df.sample(1500, random_state=42)
        fig3 = px.scatter(
            sample, x="Duration", y="Calories",
            color="Gender_Label",
            color_discrete_map={"Male": COLORS["fire"], "Female": COLORS["teal"]},
            opacity=0.55, template=TEMPLATE
        )
        fig3.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### 🔗 Feature Correlation Heatmap")
        num_cols = ["Age","Height","Weight","Duration","Heart_Rate","Body_Temp","BMI","Effort_Index","Calories"]
        corr = df[num_cols].corr()
        fig4 = px.imshow(
            corr, text_auto=".2f",
            color_continuous_scale=[[0,"#1a1a1a"],[0.5,"#ff4d1c44"],[1,"#ff4d1c"]],
            template=TEMPLATE
        )
        fig4.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

    # ── Row 3: Heart Rate vs Calories + Age Group Analysis ────────────────────
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("#### 💓 Heart Rate vs Calories")
        sample2 = df.sample(1500, random_state=7)
        fig5 = px.scatter(
            sample2, x="Heart_Rate", y="Calories",
            color="Calories",
            color_continuous_scale=["#1a1a1a","#ff4d1c","#ffe66d"],
            opacity=0.7, template=TEMPLATE
        )
        fig5.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           coloraxis_showscale=False)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("#### 🧑‍🤝‍🧑 Avg Calories by Age Group")
        df["Age_Group"] = pd.cut(df["Age"], bins=[10,20,30,40,50,60,70,80],
                                 labels=["10s","20s","30s","40s","50s","60s","70s"])
        age_grp = df.groupby("Age_Group", observed=True)["Calories"].mean().reset_index()
        fig6 = px.bar(
            age_grp, x="Age_Group", y="Calories",
            color="Calories",
            color_continuous_scale=["#ff4d1c","#ffe66d"],
            template=TEMPLATE
        )
        fig6.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

    # ── Row 4: Intensity Breakdown ────────────────────────────────────────────
    st.markdown("#### 🏋️ Workout Intensity Breakdown")
    intensity_df = df.groupby(["Intensity","Gender_Label"], observed=True).size().reset_index(name="Count")
    fig7 = px.bar(
        intensity_df, x="Intensity", y="Count", color="Gender_Label",
        barmode="group",
        color_discrete_map={"Male": COLORS["fire"], "Female": COLORS["teal"]},
        template=TEMPLATE
    )
    fig7.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10))
    st.plotly_chart(fig7, use_container_width=True)

    # ── Raw Data Preview ───────────────────────────────────────────────────────
    with st.expander("🗂 View Raw Dataset Sample (first 100 rows)"):
        st.dataframe(
            df[["Gender_Label","Age","Height","Weight","Duration",
                "Heart_Rate","Body_Temp","BMI","Calories"]].head(100),
            use_container_width=True
        )
