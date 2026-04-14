from __future__ import annotations

import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src import config


PLOT_STYLE = {
    "figure.facecolor": "#0f172a",
    "axes.facecolor": "#111827",
    "axes.edgecolor": "#94a3b8",
    "axes.labelcolor": "#e5e7eb",
    "xtick.color": "#cbd5e1",
    "ytick.color": "#cbd5e1",
    "text.color": "#f8fafc",
}


def _apply_style() -> None:
    sns.set_theme(style="darkgrid")
    plt.rcParams.update(PLOT_STYLE)


def create_visualizations(test_df: pd.DataFrame, predictions_df: pd.DataFrame) -> None:
    _apply_style()
    metrics = json.loads(config.METRICS_PATH.read_text(encoding="utf-8"))
    labels = metrics["labels"]
    confusion = pd.DataFrame(metrics["confusion_matrix"], index=labels, columns=labels)

    plt.figure(figsize=(10, 7))
    sns.heatmap(confusion, annot=True, fmt="d", cmap="crest")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(config.PLOTS_DIR / "confusion_matrix.png", dpi=200)
    plt.close()

    plt.figure(figsize=(11, 6))
    top_predictions = predictions_df["predicted_attack_type"].value_counts()
    sns.barplot(x=top_predictions.index, y=top_predictions.values, hue=top_predictions.index, palette="mako", legend=False)
    plt.title("Predicted Attack Distribution")
    plt.xlabel("Attack Type")
    plt.ylabel("Event Count")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(config.PLOTS_DIR / "attack_distribution.png", dpi=200)
    plt.close()

    plt.figure(figsize=(11, 6))
    sns.scatterplot(
        data=predictions_df,
        x="classification_confidence",
        y="risk_score",
        hue="severity",
        palette={"Low": "#93c5fd", "Medium": "#fbbf24", "High": "#fb7185", "Critical": "#ef4444"},
        alpha=0.8,
    )
    plt.title("Threat Confidence vs Risk Score")
    plt.xlabel("Classification Confidence")
    plt.ylabel("Risk Score")
    plt.tight_layout()
    plt.savefig(config.PLOTS_DIR / "risk_scatter.png", dpi=200)
    plt.close()

    timeline = predictions_df.copy()
    timeline["timestamp"] = pd.to_datetime(timeline["timestamp"])
    timeline["date"] = timeline["timestamp"].dt.date
    critical_timeline = timeline.groupby(["date", "severity"]).size().reset_index(name="count")

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=critical_timeline, x="date", y="count", hue="severity", marker="o")
    plt.title("Alert Timeline by Severity")
    plt.xlabel("Date")
    plt.ylabel("Alerts")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(config.PLOTS_DIR / "alert_timeline.png", dpi=200)
    plt.close()

    plt.figure(figsize=(11, 6))
    location_threats = predictions_df[predictions_df["predicted_attack_type"] != "normal"]["location"].value_counts()
    sns.barplot(x=location_threats.index, y=location_threats.values, hue=location_threats.index, palette="rocket", legend=False)
    plt.title("Threats by Logistics Site")
    plt.xlabel("Location")
    plt.ylabel("Threat Count")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(config.PLOTS_DIR / "location_threats.png", dpi=200)
    plt.close()
