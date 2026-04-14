from __future__ import annotations

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

from src import config
from src.utils import save_json


def build_preprocessor() -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, config.NUMERIC_COLUMNS),
            ("cat", categorical_transformer, config.CATEGORICAL_COLUMNS),
        ]
    )


def train_models(train_df: pd.DataFrame, test_df: pd.DataFrame) -> dict:
    feature_columns = config.NUMERIC_COLUMNS + config.CATEGORICAL_COLUMNS
    X_train = train_df[feature_columns]
    X_test = test_df[feature_columns]
    y_train = train_df[config.TARGET_COLUMN]
    y_test = test_df[config.TARGET_COLUMN]

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    preprocessor = build_preprocessor()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    classifier = RandomForestClassifier(
        n_estimators=220,
        max_depth=12,
        min_samples_split=5,
        class_weight="balanced",
        random_state=config.RANDOM_STATE,
    )
    classifier.fit(X_train_processed, y_train_encoded)

    benign_mask = train_df[config.TARGET_COLUMN] == "normal"
    anomaly_model = IsolationForest(
        n_estimators=180,
        contamination=0.18,
        random_state=config.RANDOM_STATE,
    )
    anomaly_model.fit(X_train_processed[benign_mask])

    probabilities = classifier.predict_proba(X_test_processed)
    predictions_encoded = classifier.predict(X_test_processed)
    predictions = label_encoder.inverse_transform(predictions_encoded)

    metrics = {
        "accuracy": round(float(accuracy_score(y_test_encoded, predictions_encoded)), 4),
        "precision_weighted": round(float(precision_score(y_test_encoded, predictions_encoded, average="weighted", zero_division=0)), 4),
        "recall_weighted": round(float(recall_score(y_test_encoded, predictions_encoded, average="weighted", zero_division=0)), 4),
        "f1_weighted": round(float(f1_score(y_test_encoded, predictions_encoded, average="weighted", zero_division=0)), 4),
        "classification_report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
        "labels": label_encoder.classes_.tolist(),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=label_encoder.classes_.tolist()).tolist(),
    }
    save_json(metrics, config.METRICS_PATH)

    joblib.dump(classifier, config.CLASSIFIER_PATH)
    joblib.dump(anomaly_model, config.ANOMALY_MODEL_PATH)
    joblib.dump(preprocessor, config.PREPROCESSOR_PATH)
    joblib.dump(label_encoder, config.LABEL_ENCODER_PATH)

    return {
        "classifier": classifier,
        "anomaly_model": anomaly_model,
        "preprocessor": preprocessor,
        "label_encoder": label_encoder,
        "X_test_processed": X_test_processed,
        "predictions": predictions,
        "probabilities": probabilities,
        "metrics": metrics,
    }

