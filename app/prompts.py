from pathlib import Path
import sys
import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.schemas import PromptConfig


def load_prompt(version: str) -> PromptConfig:
    path = ROOT_DIR / "prompts" / f"{version}.yaml"

    with open(path, "r") as file:
        data = yaml.safe_load(file)

    return PromptConfig(**data)