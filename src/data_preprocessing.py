from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src import config
from src.feature_engineering import add_engineered_features
from src.utils import ensure_directories


def load_raw_dataset(path: str | None = None) -> pd.DataFrame:
    dataset_path = path or config.RAW_DATA_PATH
    return pd.read_csv(dataset_path, parse_dates=["timestamp"])


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates(subset=["record_id"])

    numeric_columns = [
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
    for column in numeric_columns:
        cleaned[column] = cleaned[column].fillna(cleaned[column].median())
        cleaned[column] = cleaned[column].clip(lower=0)

    categorical_columns = ["location", "device_type", "protocol", "source_zone", "destination_zone", "shift", "attack_type"]
    for column in categorical_columns:
        cleaned[column] = cleaned[column].fillna("Unknown")

    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], errors="coerce")
    cleaned = cleaned.dropna(subset=["timestamp"])
    return add_engineered_features(cleaned)


def split_and_save_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_directories()
    train_df, test_df = train_test_split(
        df,
        test_size=1 - config.TRAIN_SPLIT_RATIO,
        random_state=config.RANDOM_STATE,
        stratify=df[config.TARGET_COLUMN],
    )

    rng = np.random.default_rng(config.RANDOM_STATE)
    drift_columns = [
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
        "endpoint_risk_score",
        "payload_signature_score",
    ]
    for column in drift_columns:
        test_df[column] = (test_df[column] * rng.uniform(0.92, 1.08, size=len(test_df))).clip(lower=0)

    shift_mask = rng.random(len(test_df)) < 0.04
    test_df.loc[shift_mask, "protocol"] = rng.choice(["TCP", "HTTPS", "DNS"], size=int(shift_mask.sum()))

    train_df.to_csv(config.TRAIN_DATA_PATH, index=False)
    test_df.to_csv(config.TEST_DATA_PATH, index=False)
    return train_df, test_df
