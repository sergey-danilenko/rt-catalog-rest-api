import os
from pathlib import Path
from dotenv import load_dotenv

from app.common.config import Paths


def common_get_paths(env_var: str) -> Paths:
    load_dotenv()
    if path := os.getenv(env_var):
        return Paths(Path(path))
    return Paths(Path(__file__).parent.parent.parent.parent)


def get_paths() -> Paths:
    return common_get_paths("APP_DIR")
