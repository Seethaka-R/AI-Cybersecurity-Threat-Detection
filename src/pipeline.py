from __future__ import annotations

from src.data_preprocessing import clean_dataset, load_raw_dataset, split_and_save_data
from src.detect_threats import generate_alerts
from src.generate_data import save_dataset
from src.train_model import train_models
from src.utils import ensure_directories
from src.visualize import create_visualizations


def run_full_pipeline() -> None:
    ensure_directories()
    save_dataset()
    raw_df = load_raw_dataset()
    cleaned_df = clean_dataset(raw_df)
    train_df, test_df = split_and_save_data(cleaned_df)
    model_outputs = train_models(train_df, test_df)
    predictions_df, _ = generate_alerts(
        test_df=test_df,
        predictions=model_outputs["predictions"],
        probabilities=model_outputs["probabilities"],
        anomaly_model=model_outputs["anomaly_model"],
        X_test_processed=model_outputs["X_test_processed"],
    )
    create_visualizations(test_df, predictions_df)
    print("Pipeline completed successfully.")

