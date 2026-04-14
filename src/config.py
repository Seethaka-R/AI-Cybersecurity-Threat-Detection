from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUTS_DIR / "plots"
METRICS_DIR = OUTPUTS_DIR / "metrics"
REPORTS_DIR = OUTPUTS_DIR / "reports"
DOCS_DIR = BASE_DIR / "docs"

RAW_DATA_PATH = RAW_DATA_DIR / "logistics_cyber_threat_dataset.csv"
TRAIN_DATA_PATH = PROCESSED_DATA_DIR / "train_dataset.csv"
TEST_DATA_PATH = PROCESSED_DATA_DIR / "test_dataset.csv"
ALERTS_PATH = REPORTS_DIR / "threat_alerts.csv"
PREDICTIONS_PATH = REPORTS_DIR / "predictions.csv"
SUMMARY_PATH = REPORTS_DIR / "project_summary.csv"
METRICS_PATH = METRICS_DIR / "model_metrics.json"
CLASSIFIER_PATH = MODELS_DIR / "rf_classifier.joblib"
ANOMALY_MODEL_PATH = MODELS_DIR / "isolation_forest.joblib"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.joblib"

RANDOM_STATE = 42
TRAIN_SPLIT_RATIO = 0.8
DATASET_SIZE = 4000

NUMERIC_COLUMNS = [
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
    "privilege_escalation_flag",
    "off_hours_flag",
    "geo_distance_km",
    "vpn_usage",
    "endpoint_risk_score",
    "payload_signature_score",
    "traffic_ratio",
    "auth_failure_rate",
    "bytes_per_packet",
    "session_intensity",
    "lateral_movement_score",
]

CATEGORICAL_COLUMNS = [
    "location",
    "device_type",
    "protocol",
    "source_zone",
    "destination_zone",
    "shift",
]

TARGET_COLUMN = "attack_type"
BINARY_TARGET_COLUMN = "is_threat"

