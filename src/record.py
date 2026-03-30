import csv
import os
from datetime import datetime


def write_record(record_path: str, experiment_name: str, model_name: str,
                 datasets: list[str], template_id: int) -> None:
    """將實驗紀錄寫入 record.csv（自動建立標題列）"""
    file_exists = os.path.isfile(record_path)

    with open(record_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "experiment", "model", "datasets", "template"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            experiment_name,
            model_name,
            ";".join(os.path.basename(d) for d in datasets),
            template_id,
        ])
