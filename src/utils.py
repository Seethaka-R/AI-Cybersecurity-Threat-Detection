import json
from pathlib import Path

from src import config


def ensure_directories() -> None:
    for path in [
        config.DATA_DIR,
        config.RAW_DATA_DIR,
        config.PROCESSED_DATA_DIR,
        config.MODELS_DIR,
        config.OUTPUTS_DIR,
        config.PLOTS_DIR,
        config.METRICS_DIR,
        config.REPORTS_DIR,
        config.DOCS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)

    for placeholder in [
        config.PLOTS_DIR / ".gitkeep",
        config.METRICS_DIR / ".gitkeep",
        config.REPORTS_DIR / ".gitkeep",
    ]:
        placeholder.touch(exist_ok=True)


def save_json(payload: dict, path: Path) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

