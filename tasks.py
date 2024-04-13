"""Development tasks for the cookiecutter template project."""

from pathlib import Path
import platform
from typing import Any, cast
import webbrowser

from invoke import Collection, Context, Result, task
from invokelint import _clean, dist, lint, style, test

ns = Collection()
ns.add_collection(_clean, name="clean")
ns.add_collection(dist)
ns.add_collection(lint)
ns.add_collection(style)
ns.add_collection(test)

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")


def _run(context: Context, command: str, **kwargs: Any) -> Result:
    return cast(
        Result,
        context.run(command, pty=platform.system() != "Windows", **kwargs),
    )


@task
def docs(context: Context) -> None:
    """Generate documentation."""
    _run(context, f"sphinx-build -b html {DOCS_DIR} {DOCS_BUILD_DIR}")
    webbrowser.open(DOCS_INDEX.absolute().as_uri())


ns.add_task(docs)


@task
def clean_docs(context: Context) -> None:
    """Clean up files from documentation builds."""
    _run(context, f"rm -fr {DOCS_BUILD_DIR}")


ns.add_task(clean_docs)
