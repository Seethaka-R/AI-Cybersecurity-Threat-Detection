from __future__ import annotations

import numpy as np
import pandas as pd

from src import config
from src.utils import ensure_directories


LOCATIONS = [
    "Mumbai_Hub",
    "Delhi_Distribution_Center",
    "Bengaluru_Fleet_HQ",
    "Chennai_Warehouse",
    "Pune_CrossDock",
]
DEVICE_TYPES = ["Fleet_Gateway", "Warehouse_Server", "Dispatch_Console", "Driver_Tablet", "IoT_Scanner"]
PROTOCOLS = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH"]
ZONES = ["Internet", "DMZ", "Corporate_LAN", "Warehouse_OT", "Fleet_VPN", "Cloud_API"]
SHIFTS = ["Morning", "Evening", "Night"]
ATTACK_TYPES = ["normal", "dos", "brute_force", "data_exfiltration", "malware_beaconing", "insider_scan"]


NUMERIC_PROFILE_KEYS = [
    "bytes_sent",
    "bytes_received",
    "packets",
    "session_duration_sec",
    "failed_logins",
    "login_attempts",
    "unique_ports",
    "port_entropy",
    "dns_queries",
    "file_write_ops",
    "geo_distance_km",
    "endpoint_risk_score",
    "payload_signature_score",
]


def _sample_base_row(
    rng: np.random.Generator,
    attack_type: str,
    timestamp: pd.Timestamp,
    profile_type: str | None = None,
) -> dict:
    profile_type = profile_type or attack_type
    location = rng.choice(LOCATIONS)
    device_type = rng.choice(DEVICE_TYPES)
    protocol = rng.choice(PROTOCOLS, p=[0.28, 0.12, 0.14, 0.26, 0.12, 0.08])
    source_zone = rng.choice(ZONES)
    destination_zone = rng.choice(ZONES)
    shift = rng.choice(SHIFTS, p=[0.38, 0.34, 0.28])

    base = {
        "timestamp": timestamp,
        "location": location,
        "device_type": device_type,
        "protocol": protocol,
        "source_zone": source_zone,
        "destination_zone": destination_zone,
        "shift": shift,
    }

    profiles = {
        "normal": {
            "bytes_sent": rng.normal(2400, 800),
            "bytes_received": rng.normal(3100, 900),
            "packets": rng.normal(85, 22),
            "session_duration_sec": rng.normal(410, 120),
            "failed_logins": rng.poisson(0.2),
            "login_attempts": max(1, rng.poisson(1.8)),
            "unique_ports": rng.integers(2, 8),
            "port_entropy": rng.normal(1.6, 0.35),
            "dns_queries": rng.poisson(4),
            "file_write_ops": rng.poisson(5),
            "privilege_escalation_flag": 0,
            "off_hours_flag": int(shift == "Night" and rng.random() < 0.25),
            "geo_distance_km": abs(rng.normal(35, 20)),
            "vpn_usage": int(source_zone == "Fleet_VPN" or rng.random() < 0.25),
            "endpoint_risk_score": np.clip(rng.normal(18, 10), 1, 100),
            "payload_signature_score": np.clip(rng.normal(0.18, 0.08), 0, 1),
        },
        "dos": {
            "bytes_sent": rng.normal(16000, 3000),
            "bytes_received": rng.normal(19000, 3500),
            "packets": rng.normal(520, 90),
            "session_duration_sec": rng.normal(70, 25),
            "failed_logins": rng.poisson(0.4),
            "login_attempts": max(1, rng.poisson(2.0)),
            "unique_ports": rng.integers(14, 34),
            "port_entropy": rng.normal(4.1, 0.45),
            "dns_queries": rng.poisson(10),
            "file_write_ops": rng.poisson(3),
            "privilege_escalation_flag": 0,
            "off_hours_flag": int(rng.random() < 0.55),
            "geo_distance_km": abs(rng.normal(1100, 550)),
            "vpn_usage": int(rng.random() < 0.15),
            "endpoint_risk_score": np.clip(rng.normal(73, 14), 1, 100),
            "payload_signature_score": np.clip(rng.normal(0.72, 0.12), 0, 1),
        },
        "brute_force": {
            "bytes_sent": rng.normal(1800, 500),
            "bytes_received": rng.normal(1600, 450),
            "packets": rng.normal(95, 25),
            "session_duration_sec": rng.normal(250, 80),
            "failed_logins": rng.poisson(8),
            "login_attempts": max(5, rng.poisson(14)),
            "unique_ports": rng.integers(4, 12),
            "port_entropy": rng.normal(2.4, 0.4),
            "dns_queries": rng.poisson(2),
            "file_write_ops": rng.poisson(1),
            "privilege_escalation_flag": int(rng.random() < 0.18),
            "off_hours_flag": int(rng.random() < 0.62),
            "geo_distance_km": abs(rng.normal(820, 430)),
            "vpn_usage": int(rng.random() < 0.12),
            "endpoint_risk_score": np.clip(rng.normal(68, 13), 1, 100),
            "payload_signature_score": np.clip(rng.normal(0.59, 0.14), 0, 1),
        },
        "data_exfiltration": {
            "bytes_sent": rng.normal(22500, 4200),
            "bytes_received": rng.normal(6500, 1800),
            "packets": rng.normal(160, 40),
            "session_duration_sec": rng.normal(780, 160),
            "failed_logins": rng.poisson(1),
            "login_attempts": max(1, rng.poisson(3)),
            "unique_ports": rng.integers(6, 16),
            "port_entropy": rng.normal(3.1, 0.5),
            "dns_queries": rng.poisson(8),
            "file_write_ops": rng.poisson(16),
            "privilege_escalation_flag": int(rng.random() < 0.32),
            "off_hours_flag": int(rng.random() < 0.74),
            "geo_distance_km": abs(rng.normal(1900, 760)),
            "vpn_usage": int(rng.random() < 0.08),
            "endpoint_risk_score": np.clip(rng.normal(81, 10), 1, 100),
            "payload_signature_score": np.clip(rng.normal(0.77, 0.11), 0, 1),
        },
        "malware_beaconing": {
            "bytes_sent": rng.normal(4200, 1000),
            "bytes_received": rng.normal(4800, 1200),
            "packets": rng.normal(140, 35),
            "session_duration_sec": rng.normal(620, 150),
            "failed_logins": rng.poisson(1.5),
            "login_attempts": max(1, rng.poisson(4)),
            "unique_ports": rng.integers(10, 22),
            "port_entropy": rng.normal(3.6, 0.45),
            "dns_queries": rng.poisson(14),
            "file_write_ops": rng.poisson(9),
            "privilege_escalation_flag": int(rng.random() < 0.28),
            "off_hours_flag": int(rng.random() < 0.48),
            "geo_distance_km": abs(rng.normal(1350, 620)),
            "vpn_usage": int(rng.random() < 0.2),
            "endpoint_risk_score": np.clip(rng.normal(76, 11), 1, 100),
            "payload_signature_score": np.clip(rng.normal(0.69, 0.12), 0, 1),
        },
        "insider_scan": {
            "bytes_sent": rng.normal(3200, 700),
            "bytes_received": rng.normal(2700, 750),
            "packets": rng.normal(220, 50),
            "session_duration_sec": rng.normal(540, 120),
            "failed_logins": rng.poisson(0.8),
            "login_attempts": max(1, rng.poisson(4)),
            "unique_ports": rng.integers(20, 46),
            "port_entropy": rng.normal(4.6, 0.4),
            "dns_queries": rng.poisson(5),
            "file_write_ops": rng.poisson(4),
            "privilege_escalation_flag": int(rng.random() < 0.22),
            "off_hours_flag": int(rng.random() < 0.51),
            "geo_distance_km": abs(rng.normal(120, 90)),
            "vpn_usage": int(rng.random() < 0.35),
            "endpoint_risk_score": np.clip(rng.normal(61, 12), 1, 100),
            "payload_signature_score": np.clip(rng.normal(0.53, 0.13), 0, 1),
        },
    }

    attack_features = profiles[profile_type].copy()
    for key, value in attack_features.items():
        if isinstance(value, (float, np.floating)):
            attack_features[key] = max(0.0, float(value))

    record = {**base, **attack_features}

    for key in NUMERIC_PROFILE_KEYS:
        record[key] = max(0.0, record[key] * rng.uniform(0.85, 1.15))

    if profile_type != "normal" and rng.random() < 0.28:
        record["bytes_sent"] *= rng.uniform(0.65, 0.9)
        record["bytes_received"] *= rng.uniform(0.75, 1.05)
        record["unique_ports"] *= rng.uniform(0.75, 0.95)
        record["payload_signature_score"] *= rng.uniform(0.75, 0.95)
        record["endpoint_risk_score"] *= rng.uniform(0.82, 0.97)

    if profile_type == "normal" and rng.random() < 0.09:
        record["failed_logins"] += rng.integers(1, 4)
        record["unique_ports"] += rng.integers(2, 7)
        record["payload_signature_score"] = min(1.0, record["payload_signature_score"] + rng.uniform(0.05, 0.16))
        record["endpoint_risk_score"] = min(100.0, record["endpoint_risk_score"] + rng.uniform(8, 18))

    record["is_threat"] = int(attack_type != "normal")
    record["attack_type"] = attack_type
    return record


def create_dataset(size: int = config.DATASET_SIZE, random_state: int = config.RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    attack_distribution = [0.58, 0.11, 0.1, 0.08, 0.08, 0.05]

    timestamps = pd.date_range("2026-01-01", periods=size, freq="3h")
    rows = []
    for timestamp in timestamps:
        attack_type = rng.choice(ATTACK_TYPES, p=attack_distribution)
        profile_type = attack_type

        if attack_type == "normal" and rng.random() < 0.05:
            profile_type = rng.choice(["brute_force", "insider_scan", "malware_beaconing"])
        elif attack_type != "normal" and rng.random() < 0.14:
            candidate_profiles = [item for item in ATTACK_TYPES if item not in [attack_type]]
            profile_type = rng.choice(candidate_profiles)

        rows.append(_sample_base_row(rng, attack_type, timestamp, profile_type=profile_type))

    df = pd.DataFrame(rows)
    df["record_id"] = [f"LOGSEC-{index:05d}" for index in range(1, len(df) + 1)]
    df = df[
        ["record_id", "timestamp", "location", "device_type", "protocol", "source_zone", "destination_zone", "shift",
         "bytes_sent", "bytes_received", "packets", "session_duration_sec", "failed_logins", "login_attempts",
         "unique_ports", "port_entropy", "dns_queries", "file_write_ops", "privilege_escalation_flag",
         "off_hours_flag", "geo_distance_km", "vpn_usage", "endpoint_risk_score", "payload_signature_score",
         "attack_type", "is_threat"]
    ]
    return df


def save_dataset(size: int = config.DATASET_SIZE) -> pd.DataFrame:
    ensure_directories()
    dataset = create_dataset(size=size)
    dataset.to_csv(config.RAW_DATA_PATH, index=False)
    return dataset


if __name__ == "__main__":
    generated = save_dataset()
    print(f"Generated dataset with {len(generated)} rows at {config.RAW_DATA_PATH}")
