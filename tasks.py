"""Development tasks for the cookiecutter template project"""

import platform
import webbrowser
from pathlib import Path

from invoke import task
from invoke.runners import Failure

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
TEST_DIR = ROOT_DIR.joinpath("tests")
SETUP_PY = ROOT_DIR.joinpath("setup.py")
TASK_PY = ROOT_DIR.joinpath("tasks.py")
PYTHON_DIRS = [str(d) for d in [SETUP_PY, TASK_PY, TEST_DIR]]


def _run(c, command, **kwargs):
    return c.run(command, pty=platform.system() != "Windows", **kwargs)


@task
def test(c):
    """
    Run tests
    """
    _run(c, "pytest")


@task(help={"check": "Checks if source is formatted without applying changes"})
def format(c, check=False):
    """
    Format code
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    list_result = []
    # Run isort
    isort_options = "--recursive {}".format("--check-only" if check else "")
    list_result.append(
        _run(c, "isort {} {}".format(isort_options, python_dirs_string), warn=True)
    )
    # Run pipenv-setup
    isort_options = "{}".format("check --strict" if check else "sync --pipfile")
    list_result.append(_run(c, "pipenv-setup {}".format(isort_options), warn=True))
    # Run black
    black_options = "{}".format("--check --diff" if check else "")
    list_result.append(
        _run(c, "black {} {}".format(black_options, python_dirs_string), warn=True)
    )
    for result in list_result:
        if result.failed:
            raise Failure(result)


@task
def docs(c):
    """
    Generate documentation
    """
    _run(c, "sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))
    webbrowser.open(DOCS_INDEX.absolute().as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    _run(c, "rm -fr {}".format(DOCS_BUILD_DIR))
