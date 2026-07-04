# Developer Guide

## Purpose

This document explains the role of each file in the repository and how the experiment is assembled.

## Root files

- `version_eval.py`
  - Main execution entrypoint for the experiment.
  - Creates an `Evaluator` for a chosen prompt version.
  - Prints a console summary and saves the final prompt-version report.

- `requirements.txt`
  - Lists Python dependencies required by the project.
  - Includes `langchain-ollama`, `pydantic`, `pyyaml`, and `langchain` packages.

- `LICENSE`
  - Defines repository licensing terms.

## app/

- `app/__init__.py`
  - Package initializer. Keeps the `app` directory importable.

- `app/config.py`
  - Central configuration values for the experiment.
  - Defines `MODEL_NAME`, `TEMPERATURE`, `SEED`, and `REPORT_PATH`.

- `app/evaluate.py`
  - Contains `Evaluator`.
  - Loads the golden dataset and evaluates each sample.
  - Measures latency and computes accuracy.
  - Saves results to `results/` and returns an `EvaluationReport`.

- `app/llm.py`
  - Defines the LLM client using `ChatOllama`.
  - Applies model settings from `app/config.py`.

- `app/classifier.py`
  - Implements `classify_email()`.
  - Loads prompt configuration and sends the prompt + email to the LLM.
  - Uses structured output based on `app.schemas.EmailResult`.
  - Includes fallback handling for LLM connection failures.

- `app/prompts.py`
  - Loads prompt YAML files from the `prompts/` directory.
  - Converts YAML into `app.schemas.PromptConfig`.

- `app/report.py`
  - Saves prompt-version summary reports to `reports/`.
  - Used by both `version_eval.py` and `app/evaluate.py` through `report_update`.

- `app/schemas.py`
  - Defines Pydantic models for typed data structures.
  - Contains `PromptConfig`, `EmailCategory`, `EmailResult`, `EvaluationResult`, and `EvaluationReport`.

## prompts/

- `prompts/v1.yaml`
- `prompts/v2.yaml`
- `prompts/v3.yaml`

Each YAML defines a prompt version with:
- `version`
- `created_at`
- `description`
- `system_prompt`

The prompt instructs the LLM to classify emails and produce structured output.

## dataset/

- `dataset/golden_dataset_v1.json`
  - The ground truth dataset used for evaluation.
  - Each sample includes `id`, `email`, `expected_category`, `expected_summary`, and metadata fields like `difficulty` and `notes`.

## reports/

- `reports/v1.json`
- `reports/v2.json`
- `reports/v3.json`

These files store the aggregated summary for each prompt version.

## results/

- `results/run_001.json`, `run_002.json`, etc.

Each run file is a detailed evaluation report generated during execution. It includes per-sample predictions, pass/fail flags, and latency.

## Running and extending

1. Install dependencies via `pip install -r requirements.txt`.
2. Run the experiment with `python version_eval.py`.
3. Add new prompt versions by creating `prompts/vX.yaml` and updating `version_eval.py` if needed.
4. Add new dataset versions by adding JSON files under `dataset/` and updating `app/evaluate.py` dataset path if required.

## Notes for developers

- The experiment is prompt-version driven; changing prompt YAML files is the normal way to iterate.
- `app/schemas.py` defines the exact structured output expected from the LLM.
- The `results/` directory is used for detailed debugging, while `reports/` is used for high-level benchmarking.
- Current evaluation code includes a fixed `10` second pause between requests in `app/evaluate.py`.
