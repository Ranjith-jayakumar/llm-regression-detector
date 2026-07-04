import json
from pathlib import Path

REPORTS_DIR = Path("reports")


def compare_reports():

    reports = []

    for file in REPORTS_DIR.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:
            reports.append(json.load(f))

    reports.sort(key=lambda x: x["accuracy"], reverse=True)

    print("=" * 50)
    print("Prompt Comparison Report")
    print("=" * 50)

    for report in reports:

        print(
            f"""
Prompt Version : {report['prompt_version']}
Accuracy       : {report['accuracy']}%
Passed Cases   : {report['passed_cases']}
Failed Cases   : {report['failed_cases']}
"""
        )

    best = reports[0]

    print("=" * 50)
    print("Best Prompt")
    print("=" * 50)

    print(
        f"""
Prompt Version : {best['prompt_version']}

Reason:
- Highest Accuracy : {best['accuracy']}%
- Passed Cases     : {best['passed_cases']}
- Failed Cases     : {best['failed_cases']}
"""
    )
compare_reports()