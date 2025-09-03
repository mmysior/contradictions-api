import json
from typing import List

from app.core.config import settings
from app.schemas.parameters import Parameter
from app.schemas.principles import Principle


def load_json_data(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_parameters() -> List[Parameter]:
    parameters_data = load_json_data(str(settings.PARAMETERS_FILE_PATH))
    return [Parameter(**p) for p in parameters_data["parameters"]]


def get_principles() -> List[Principle]:
    principles_data = load_json_data(str(settings.PRINCIPLES_FILE_PATH))
    return [Principle(**p) for p in principles_data]
