from langchain_ollama import ChatOllama

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import MODEL_NAME, TEMPERATURE, SEED

def define_llm():
    return ChatOllama(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        seed=SEED
    )