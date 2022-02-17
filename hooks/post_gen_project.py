# Copyright (c) 2022 Microsoft
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
import shutil
import warnings
from pathlib import Path
from typing import NamedTuple

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import RepositoryNotFound, RepositoryCloneFailed


class Submodule(NamedTuple):
    label: str
    choice: str
    url_file: Path
    target_directory: str


CI_CD_CHOICE = "{{ cookiecutter['CI/CD Service'] }}"
CI_CD_FOLDER_NAMES = {
    "Github Actions": ".github",
    "Azure DevOps": ".azuredevops"
}

EMPTY_FOLDERS = [
    Path('.azuredevops'),
    Path('.cloud'),
    Path('.github'),
    Path('project')
]

SUBMODULES = [
    Submodule(
        label="CI/CD",
        choice=CI_CD_CHOICE,
        url_file=Path("./ci-cd-urls.json"),
        target_directory=CI_CD_FOLDER_NAMES[CI_CD_CHOICE]
    ),
    Submodule(
        label="project",
        choice="{{ cookiecutter['Project Template'] }}",
        url_file=Path("./project-urls.json"),
        target_directory="project"
    ),
    Submodule(
        label="infrastructure",
        choice="{{ cookiecutter['Infrastructure Template'] }}",
        url_file=Path("./cloud-infra-urls.json"),
        target_directory=".cloud"
    ),
]


def read_json(file_path: Path) -> dict:
    with open(file_path, 'r') as json_file:
        results = json.load(json_file)

    return results


def process_submodule(module: Submodule) -> None:
    if not module.url_file.exists():
        warnings.warn(
            f"For '{module.label}': Required file {module.url_file.absolute()} was not found"
        )
        return None

    # Read JSON file
    urls = read_json(module.url_file)

    if module.choice not in urls.keys():
        warnings.warn(
            f"For '{module.label}': Selected value '{module.choice}' not found in {module.url_file.absolute()}"
        )
        return None

    chosen_url = urls[module.choice]

    # Invoke cookiecutter
    if chosen_url:
        try:
            print(f"Pulling {module.label} files")
            cookiecutter(
                template=chosen_url,
                no_input=True,
                default_config=True,
                extra_context={'directory': module.target_directory}
            )
        except RepositoryCloneFailed:
            warnings.warn(
                f"For '{module.label}': The cookiecutter repo at '{chosen_url}' failed to clone"
            )

        except RepositoryNotFound:
            warnings.warn(
                f"For '{module.label}': A cookiecutter repo wasn't found at '{chosen_url}'"
            )
    else:
        warnings.warn(
            f"For '{module.label}': URL was not set, skipping '{module.label}'"
        )


def add_submodules():
    # Remove empty folders
    for folder in EMPTY_FOLDERS:
        shutil.rmtree(path=folder, ignore_errors=True)

    # Loop through submodules and process
    for module in SUBMODULES:
        process_submodule(module)
        
        # Remove the JSON configuration file
        module.url_file.unlink()

if __name__ == "__main__":
    add_submodules()
