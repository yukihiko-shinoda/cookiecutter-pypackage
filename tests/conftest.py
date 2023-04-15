"""Configuration for pytest."""
from typing import Generator

from cookiecutter.utils import rmtree
import pytest
from pytest_cookies.plugin import Cookies, Result


def _process_result(result: Result) -> Generator[Result, None, None]:
    if result.exit_code:
        raise AssertionError(result.exception) from result.exception
    yield result


def process_result(result: Result) -> Generator[Result, None, None]:
    try:
        yield from _process_result(result)
    finally:
        rmtree(str(result.project))


@pytest.fixture()
def baked_in_temp_dir(
    cookies: Cookies,
    request: pytest.FixtureRequest,
) -> Generator[Result, None, None]:
    """Delete the temporal directory that is created when executing the tests.

    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    extra_context = getattr(request, "param", None)
    extra_context = {} if extra_context is None else request.param
    result = cookies.bake(extra_context=extra_context)
    yield from process_result(result)
