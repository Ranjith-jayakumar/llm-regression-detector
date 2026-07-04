from app.evaluate import Evaluator
from app.report import report_update
version="v3"
evaluator = Evaluator(prompt_version=version)

print(f"=========starting evaluarting {version}=======")
report = evaluator.evaluate()

report_update(report=report)
print()

print("========== SUMMARY ==========")

print(f"Prompt Version : {report.prompt_version}")

print(f"Accuracy       : {report.accuracy}%")

print(f"Passed         : {report.passed_cases}")

print(f"Failed         : {report.failed_cases}")