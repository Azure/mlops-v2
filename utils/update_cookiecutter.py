# Copyright (c) 2022 Microsoft
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import json
from collections import OrderedDict
from pathlib import Path
from typing import Dict

COOKIECUTTER_JSON = Path("cookiecutter.json")
KEY_TO_FILE_IDX = {
    "CI/CD Service": Path("./{{ cookiecutter['Project Directory'] }}/ci-cd-urls.json"),
    "Infrastructure Template": Path("./{{ cookiecutter['Project Directory'] }}/cloud-infra-urls.json"),
    "Project Template": Path("./{{ cookiecutter['Project Directory'] }}/project-urls.json")
}


def read_json(file_path: Path) -> Dict[str, str]:
    with open(file_path, 'r') as json_file:
        dict_obj = json.load(
            json_file, object_pairs_hook=OrderedDict)

    return dict_obj


def save_json(file_path: Path, contents: Dict[str, str]) -> None:
    with open(file_path, "w") as json_file:
        json.dump(contents, json_file, indent=4)


def update_choices():
    """Updates the choices in cookiecutter.json by reading available options in the individual index files"""
    cc_settings = read_json(COOKIECUTTER_JSON)

    for key, file in KEY_TO_FILE_IDX.items():
        key_settings = read_json(file)

        choices = list(key_settings.keys())

        cc_settings[key] = choices

        save_json(COOKIECUTTER_JSON, cc_settings)


if __name__ == "__main__":
    update_choices()
