from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
PREDICTIONS_PATH = BASE_DIR / "outputs" / "reports" / "predictions.csv"
ALERTS_PATH = BASE_DIR / "outputs" / "reports" / "threat_alerts.csv"
METRICS_PATH = BASE_DIR / "outputs" / "metrics" / "model_metrics.json"


st.set_page_config(
    page_title="Logistics Threat Detection Dashboard",
    page_icon="shield",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(56, 189, 248, 0.22), transparent 28%),
            radial-gradient(circle at top right, rgba(148, 163, 184, 0.24), transparent 32%),
            linear-gradient(135deg, #050816 0%, #0b1120 38%, #111827 100%);
        color: #e2e8f0;
    }
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 1rem;
    }
    .hero {
        padding: 1.2rem 1.4rem;
        border: 1px solid rgba(148,163,184,0.24);
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(15,23,42,0.94), rgba(30,41,59,0.72));
        box-shadow: 0 0 30px rgba(56,189,248,0.12);
        margin-bottom: 1rem;
    }
    .metric-card {
        padding: 0.9rem 1rem;
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(15,23,42,0.96), rgba(71,85,105,0.24));
        border: 1px solid rgba(148,163,184,0.18);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 12px 24px rgba(0,0,0,0.18);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_artifacts() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    predictions = pd.read_csv(PREDICTIONS_PATH, parse_dates=["timestamp"])
    alerts = pd.read_csv(ALERTS_PATH, parse_dates=["timestamp"])
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return predictions, alerts, metrics


if not PREDICTIONS_PATH.exists():
    st.error("Run `python main.py` first to generate the dataset, model, and dashboard artifacts.")
    st.stop()

predictions_df, alerts_df, metrics = load_artifacts()

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom:0.2rem;">AI-Powered Cybersecurity Threat Detection System</h1>
        <p style="margin:0;color:#cbd5e1;">
            Logistics and transportation SOC simulation with hybrid ML-based threat detection,
            metallic robotics-themed visual analytics, and recruiter-friendly proof of work.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
summary_cards = [
    ("Accuracy", f"{metrics['accuracy'] * 100:.2f}%"),
    ("Weighted F1", f"{metrics['f1_weighted'] * 100:.2f}%"),
    ("Threat Events", f"{int((predictions_df['predicted_attack_type'] != 'normal').sum())}"),
    ("Critical Alerts", f"{int((predictions_df['severity'] == 'Critical').sum())}"),
]

for column, (title, value) in zip([col1, col2, col3, col4], summary_cards):
    column.markdown(
        f"<div class='metric-card'><div style='font-size:0.9rem;color:#94a3b8;'>{title}</div>"
        f"<div style='font-size:1.8rem;font-weight:700;color:#f8fafc;'>{value}</div></div>",
        unsafe_allow_html=True,
    )

chart_col1, chart_col2 = st.columns([1.3, 1])

with chart_col1:
    threat_counts = predictions_df["predicted_attack_type"].value_counts().reset_index()
    threat_counts.columns = ["attack_type", "count"]
    attack_fig = px.bar(
        threat_counts,
        x="attack_type",
        y="count",
        color="count",
        color_continuous_scale=["#94a3b8", "#38bdf8", "#ef4444"],
        title="Predicted Attack Distribution",
    )
    attack_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
    st.plotly_chart(attack_fig, use_container_width=True)

with chart_col2:
    severity_counts = predictions_df["severity"].value_counts().reset_index()
    severity_counts.columns = ["severity", "count"]
    severity_fig = px.pie(
        severity_counts,
        names="severity",
        values="count",
        hole=0.45,
        color="severity",
        color_discrete_map={"Low": "#38bdf8", "Medium": "#f59e0b", "High": "#fb7185", "Critical": "#ef4444"},
        title="Alert Severity Split",
    )
    severity_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", legend_font_color="#e2e8f0")
    st.plotly_chart(severity_fig, use_container_width=True)

timeline = predictions_df.copy()
timeline["date"] = timeline["timestamp"].dt.date
timeline_summary = timeline.groupby(["date", "severity"]).size().reset_index(name="count")
timeline_fig = px.line(
    timeline_summary,
    x="date",
    y="count",
    color="severity",
    markers=True,
    color_discrete_map={"Low": "#38bdf8", "Medium": "#f59e0b", "High": "#fb7185", "Critical": "#ef4444"},
    title="Threat Timeline Across Logistics Operations",
)
timeline_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
st.plotly_chart(timeline_fig, use_container_width=True)

bottom_col1, bottom_col2 = st.columns([1.1, 1.2])

with bottom_col1:
    scatter_fig = px.scatter(
        predictions_df,
        x="classification_confidence",
        y="risk_score",
        color="severity",
        hover_data=["location", "device_type", "predicted_attack_type"],
        size="packets",
        color_discrete_map={"Low": "#38bdf8", "Medium": "#f59e0b", "High": "#fb7185", "Critical": "#ef4444"},
        title="Confidence vs Risk Score",
    )
    scatter_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
    st.plotly_chart(scatter_fig, use_container_width=True)

with bottom_col2:
    location_summary = (
        predictions_df[predictions_df["predicted_attack_type"] != "normal"]["location"]
        .value_counts()
        .reset_index()
    )
    location_summary.columns = ["location", "count"]
    radar_fig = go.Figure()
    radar_fig.add_trace(
        go.Scatterpolar(
            r=location_summary["count"],
            theta=location_summary["location"],
            fill="toself",
            line=dict(color="#38bdf8"),
            fillcolor="rgba(56, 189, 248, 0.28)",
            name="Threat Concentration",
        )
    )
    radar_fig.update_layout(
        title="Threat Concentration by Logistics Site",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(gridcolor="rgba(148,163,184,0.25)", linecolor="rgba(148,163,184,0.25)"),
            angularaxis=dict(gridcolor="rgba(148,163,184,0.25)", linecolor="rgba(148,163,184,0.25)"),
        ),
    )
    st.plotly_chart(radar_fig, use_container_width=True)

st.subheader("High Priority Alerts")
st.dataframe(
    alerts_df.sort_values(by="risk_score", ascending=False)[
        ["record_id", "timestamp", "location", "device_type", "predicted_attack_type", "risk_score", "severity", "alert_message"]
    ],
    use_container_width=True,
    height=320,
)

