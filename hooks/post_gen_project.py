"""Post hook of generating project."""

import os
from pathlib import Path
import shutil

PROJECT_DIRECTORY = Path(os.path.realpath(os.path.curdir))
LICENSE_DIRECTORY = PROJECT_DIRECTORY / "licenses"
PYOROJECTTOML_TEMPLATE = PROJECT_DIRECTORY / "pyproject.dist.toml"
PYOROJECTTOML = PROJECT_DIRECTORY / "pyproject.toml"


def remove_file(filepath: Path) -> None:
    (PROJECT_DIRECTORY / filepath).unlink()


def prepare_license(key_license: str) -> None:
    """Prepares license file."""
    license_file = {
        "MIT": "mit.txt",
        "GPL-3.0-or-later": "gpl3.0_github.txt",
        "Apache-2.0": "apache2.0_github.txt",
        "BSD-3-Clause": "bsd3clause.txt",
        "GPL-3.0-or-later-short": "gpl3.0_gnu.txt",
        "Apache-2.0-short": "apache2.0_apache.txt",
    }.get(key_license)
    if not license_file:
        raise ValueError(key_license)
    shutil.copy(
        LICENSE_DIRECTORY / license_file,
        PROJECT_DIRECTORY / "LICENSE",
    )


if __name__ == "__main__":
    # Reason: Detected Cookiecutter code as Literal.
    # pylint: disable=line-too-long,comparison-of-constants
    if "{{ cookiecutter.use_pypi_deployment_with_github_actions }}" != "y":  # type: ignore[comparison-overlap]  # noqa: PLR0133,E501,RUF100
        remove_file(Path(".github/workflows/deploy.yml"))
    if "{{ cookiecutter.use_pytest }}" != "y":  # type: ignore[comparison-overlap]  # noqa: PLR0133,E501,RUF100
        remove_file(Path("tests/conftest.py"))
    if "{{ cookiecutter.use_pyup }}" == "n":  # type: ignore[comparison-overlap]  # noqa: PLR0133,E501,RUF100
        remove_file(Path(".pyup.yml"))
    if "no" in "{{ cookiecutter.command_line_interface|lower }}":  # noqa: PLR0133
        cli_file = Path("{{ cookiecutter.project_slug }}") / "cli.py"
        remove_file(Path(cli_file))
    if "Not open source" != "{{ cookiecutter.open_source_license }}":  # type: ignore[comparison-overlap]  # noqa: PLR0133,E501,RUF100
        prepare_license("{{ cookiecutter.open_source_license }}")
    shutil.rmtree(LICENSE_DIRECTORY)
    PYOROJECTTOML_TEMPLATE.rename(PYOROJECTTOML)
