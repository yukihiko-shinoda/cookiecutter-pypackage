# Copyright (c) 2013-2026 Audrey Roy Greenfeld, Yukihiko Shinoda and individual contributors.
"""Pre hook of generating project."""

import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
# PEP 503 -- Simple Repository API:
#   https://peps.python.org/pep-0503/#normalized-names
PYPI_DISTRIBUTION_NAME_REGEX = r"^([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$"

MODULE_NAME = "{{ cookiecutter.project_slug}}"
PYPI_DISTRIBUTION_NAME = "{{ cookiecutter.pypi_distribution_name }}"

if not re.match(MODULE_REGEX, MODULE_NAME):
    # Reason: Specification.
    print(  # noqa: T201
        f"ERROR: The project slug ({MODULE_NAME}) is not a valid Python module name."
        " Please do not use a - and use _ instead",
    )
    # Exit to cancel project
    sys.exit(1)

if not re.match(PYPI_DISTRIBUTION_NAME_REGEX, PYPI_DISTRIBUTION_NAME):
    # Reason: Specification.
    print(  # noqa: T201
        f"ERROR: The PyPI distribution name ({PYPI_DISTRIBUTION_NAME}) is not a valid"
        " PyPI project name. See PEP 503 for the naming rule.",
    )
    # Exit to cancel project
    sys.exit(1)
