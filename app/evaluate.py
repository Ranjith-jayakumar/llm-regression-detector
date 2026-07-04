import json
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.classifier import classify_email
from app.schemas import EvaluationResult, EvaluationReport, EmailCategory

DATASET_PATH = ROOT_DIR / "dataset" / "golden_dataset_v1.json"
RESULTS_DIR = ROOT_DIR / "results"


class Evaluator:

    def __init__(self, prompt_version: str = "v1"):
        self.prompt_version = prompt_version

    def load_dataset(self):

        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate(self):

        dataset = self.load_dataset()

        evaluation_results = []

        passed = 0

        for sample in dataset:

            start = time.perf_counter()

            prediction = classify_email(
                sample["email"],
                prompt_version=self.prompt_version
            )

            end = time.perf_counter()

            latency_ms = round((end - start) * 1000, 2)

            expected_category = EmailCategory(
                sample["expected_category"]
            )

            predicted_category = prediction.category

            is_pass = expected_category == predicted_category

            if is_pass:
                passed += 1

            result = EvaluationResult(

                id=sample["id"],

                expected_category=expected_category,

                predicted_category=predicted_category,

                expected_summary=sample["expected_summary"],

                predicted_summary=prediction.summary,

                passed=is_pass,

                latency_ms=latency_ms

            )

            evaluation_results.append(result)
            time.sleep(10)
        total = len(dataset)

        failed = total - passed

        accuracy = round((passed / total) * 100, 2)

        report = EvaluationReport(

            prompt_version=self.prompt_version,

            total_cases=total,

            passed_cases=passed,

            failed_cases=failed,

            accuracy=accuracy,

            results=evaluation_results

        )

        self.save_report(report)

        return report

    def save_report(self, report: EvaluationReport):

        Path(RESULTS_DIR).mkdir(exist_ok=True)

        existing = sorted(Path(RESULTS_DIR).glob("run_*.json"))

        run_number = len(existing) + 1

        filename = Path(RESULTS_DIR) / f"run_{run_number:03d}.json"

        with open(filename, "w", encoding="utf-8") as f:

            json.dump(
                report.model_dump(mode="json"),
                f,
                indent=4
            )

        print(f"\nEvaluation report saved to {filename}")


if __name__ == "__main__":
    evaluator = Evaluator(prompt_version="v1")
    report = evaluator.evaluate()
    
    print()
    print("========== SUMMARY ==========")
    print(f"Prompt Version : {report.prompt_version}")
    print(f"Accuracy       : {report.accuracy}%")
    print(f"Passed         : {report.passed_cases}")
    print(f"Failed         : {report.failed_cases}")
