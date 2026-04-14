from __future__ import annotations

import numpy as np
import pandas as pd

from src import config


def _severity_from_score(risk_score: float) -> str:
    if risk_score >= 76:
        return "Critical"
    if risk_score >= 62:
        return "High"
    if risk_score >= 46:
        return "Medium"
    return "Low"


def generate_alerts(
    test_df: pd.DataFrame,
    predictions: np.ndarray,
    probabilities: np.ndarray,
    anomaly_model,
    X_test_processed,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    predicted_probability = probabilities.max(axis=1)
    anomaly_flags = anomaly_model.predict(X_test_processed)
    anomaly_scores = anomaly_model.decision_function(X_test_processed)

    alerts_df = test_df.copy().reset_index(drop=True)
    alerts_df["predicted_attack_type"] = predictions
    alerts_df["classification_confidence"] = (predicted_probability * 100).round(2)
    alerts_df["anomaly_flag"] = np.where(anomaly_flags == -1, 1, 0)
    alerts_df["anomaly_score"] = anomaly_scores.round(4)

    anomaly_risk = np.clip((0.04 - anomaly_scores) * 90, 0, 24)
    class_risk = np.where(alerts_df["predicted_attack_type"] == "normal", 7, 28) + (predicted_probability * 22)
    payload_risk = alerts_df["payload_signature_score"] * 14
    alerts_df["risk_score"] = np.clip(class_risk + anomaly_risk + payload_risk, 0, 100).round(2)
    alerts_df["severity"] = alerts_df["risk_score"].apply(_severity_from_score)

    alerts_df["alert_message"] = (
        "Potential "
        + alerts_df["predicted_attack_type"].str.replace("_", " ")
        + " detected at "
        + alerts_df["location"]
        + " via "
        + alerts_df["device_type"]
    )

    predictions_df = alerts_df[
        [
            "record_id",
            "timestamp",
            "location",
            "device_type",
            "packets",
            "attack_type",
            "predicted_attack_type",
            "is_threat",
            "classification_confidence",
            "anomaly_flag",
            "anomaly_score",
            "risk_score",
            "severity",
            "alert_message",
        ]
    ].sort_values(by="risk_score", ascending=False)

    high_priority_alerts = predictions_df[predictions_df["severity"].isin(["Critical", "High"])].copy()
    high_priority_alerts.to_csv(config.ALERTS_PATH, index=False)
    predictions_df.to_csv(config.PREDICTIONS_PATH, index=False)

    summary = pd.DataFrame(
        {
            "metric": [
                "total_test_events",
                "predicted_threats",
                "critical_alerts",
                "high_alerts",
                "top_detected_attack",
            ],
            "value": [
                len(predictions_df),
                int((predictions_df["predicted_attack_type"] != "normal").sum()),
                int((predictions_df["severity"] == "Critical").sum()),
                int((predictions_df["severity"] == "High").sum()),
                predictions_df["predicted_attack_type"].mode().iloc[0],
            ],
        }
    )
    summary.to_csv(config.SUMMARY_PATH, index=False)
    return predictions_df, high_priority_alerts
