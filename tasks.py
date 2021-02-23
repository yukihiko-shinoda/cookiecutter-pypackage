"""Development tasks for the cookiecutter template project"""

import platform
import webbrowser
from pathlib import Path

from invoke import task  # type: ignore
from invoke.runners import Failure, Result  # type: ignore

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
TEST_DIR = ROOT_DIR.joinpath("tests")
SETUP_PY = ROOT_DIR.joinpath("setup.py")
TASKS_PY = ROOT_DIR.joinpath("tasks.py")
PYTHON_DIRS = [str(d) for d in [SETUP_PY, TASKS_PY, TEST_DIR]]


def _run(context, command, **kwargs):
    return context.run(command, pty=platform.system() != "Windows", **kwargs)


@task
def test(context):
    """
    Run tests
    """
    _run(context, "pytest")


@task(help={"check": "Checks if source is formatted without applying changes"})
def style(context, check=False):
    """
    Format code
    """
    for result in [
        isort(context, check),
        pipenv_setup(context, check),
        black(context, check),
    ]:
        if result.failed:
            raise Failure(result)


def isort(context, check=False) -> Result:
    """Runs isort."""
    isort_options = "{}".format("--check-only --diff" if check else "")
    return _run(
        context, "isort {} {}".format(isort_options, " ".join(PYTHON_DIRS)), warn=True
    )


def pipenv_setup(context, check=False) -> Result:
    """Runs pipenv-setup."""
    isort_options = "{}".format("check --strict" if check else "sync --pipfile")
    return _run(context, "pipenv-setup {}".format(isort_options), warn=True)


def black(context, check=False) -> Result:
    """Runs black."""
    black_options = "{}".format("--check --diff" if check else "")
    return _run(
        context, "black {} {}".format(black_options, " ".join(PYTHON_DIRS)), warn=True
    )


@task
def lint_flake8(context):
    """
    Lint code with flake8
    """
    _run(context, "flake8 {} {}".format("--radon-show-closures", " ".join(PYTHON_DIRS)))


@task
def lint_pylint(context):
    """
    Lint code with pylint
    """
    _run(context, "pylint {}".format(" ".join(PYTHON_DIRS)))


@task
def lint_mypy(context):
    """
    Lint code with pylint
    """
    _run(context, "mypy {}".format(" ".join(PYTHON_DIRS)))


@task(lint_flake8, lint_pylint, lint_mypy)
def lint(_context):
    """
    Run all linting
    """


@task
def radon_cc(context):
    """
    Reports code complexity.
    """
    _run(context, "radon cc {}".format(" ".join(PYTHON_DIRS)))


@task
def radon_mi(context):
    """
    Reports maintainability index.
    """
    _run(context, "radon mi {}".format(" ".join(PYTHON_DIRS)))


@task(radon_cc, radon_mi)
def radon(_context):
    """
    Reports radon.
    """


@task
def xenon(context):
    """
    Check code complexity.
    """
    _run(
        context,
        "xenon --max-absolute A --max-modules A --max-average A {}".format(
            " ".join(PYTHON_DIRS)
        ),
    )


@task
def docs(context):
    """
    Generate documentation
    """
    _run(context, "sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))
    webbrowser.open(DOCS_INDEX.absolute().as_uri())


@task
def clean_docs(context):
    """
    Clean up files from documentation builds
    """
    _run(context, "rm -fr {}".format(DOCS_BUILD_DIR))
