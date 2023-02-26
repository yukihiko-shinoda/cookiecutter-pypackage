"""Configuration for pytest."""
from typing import Generator

from cookiecutter.utils import rmtree
import pytest
from pytest import FixtureRequest
from pytest_cookies.plugin import Cookies, Result


def process_result(result: Result) -> Generator[Result, None, None]:
    try:
        if result.exit_code:
            raise AssertionError(result.exception) from result.exception
        yield result
    finally:
        rmtree(str(result.project))


@pytest.fixture
def baked_in_temp_dir(
    cookies: Cookies, request: FixtureRequest
) -> Generator[Result, None, None]:
    """Delete the temporal directory that is created when executing the tests.

    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    extra_context = getattr(request, "param", None)
    if extra_context is None:
        extra_context = {}
    else:
        extra_context = request.param
    result = cookies.bake(extra_context=extra_context)
    yield from process_result(result)
