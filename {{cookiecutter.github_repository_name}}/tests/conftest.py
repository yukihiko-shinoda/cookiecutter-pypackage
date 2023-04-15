"""Configuration of pytest."""

from typing import Any

import pytest

collect_ignore = ["setup.py"]

@pytest.fixture()
def response() -> dict[Any, Any] | None:
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests  # noqa: ERA001
    # return requests.get("https://github.com/audreyr/cookiecutter-pypackage")  # noqa: E501,ERA001
    return None
