from __future__ import annotations

import numpy as np
import pandas as pd


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["traffic_ratio"] = enriched["bytes_sent"] / (enriched["bytes_received"] + 1)
    enriched["auth_failure_rate"] = enriched["failed_logins"] / (enriched["login_attempts"] + 1)
    enriched["bytes_per_packet"] = (enriched["bytes_sent"] + enriched["bytes_received"]) / (enriched["packets"] + 1)
    enriched["session_intensity"] = enriched["packets"] / (enriched["session_duration_sec"] + 1)
    enriched["lateral_movement_score"] = (
        enriched["unique_ports"] * 0.35
        + enriched["port_entropy"] * 0.25
        + enriched["privilege_escalation_flag"] * 4
        + enriched["vpn_usage"] * 1.5
    )

    for column in ["traffic_ratio", "auth_failure_rate", "bytes_per_packet", "session_intensity"]:
        enriched[column] = enriched[column].replace([np.inf, -np.inf], 0)

    return enriched

