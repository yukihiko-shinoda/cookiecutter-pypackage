"""Development tasks for the cookiecutter template project."""

import platform
import webbrowser
from pathlib import Path
from typing import Any
from typing import cast

from invoke import Collection
from invoke import Context
from invoke import Result
from invoke import task
from invokelint import _clean
from invokelint import dist
from invokelint import lint
from invokelint import style
from invokelint import test

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


# Reason: The kwargs can't be annotated with a specific type,
# as it can take any keyword argument.
def _run(context: Context, command: str, **kwargs: Any) -> Result:  # noqa: ANN401
    return cast(
        "Result",
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
