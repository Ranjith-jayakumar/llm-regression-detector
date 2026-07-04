import json
from pathlib import Path

from app.config import REPORT_PATH


def save_report(report):

    Path(REPORT_PATH).mkdir(parents=True, exist_ok=True)

    filename = Path(REPORT_PATH) / f"{report.prompt_version}.json"

    data = {
        "prompt_version": report.prompt_version,
        "accuracy": report.accuracy,
        "passed_cases": report.passed_cases,
        "failed_cases": report.failed_cases,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved report to {filename}")


# Backwards-compatible alias expected by main.py
report_update = save_report