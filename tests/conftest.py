"""Configuration for pytest"""
import pytest
from cookiecutter.utils import rmtree


def process_result(result):
    try:
        if result.exit_code:
            raise AssertionError(result.exception) from result.exception
        yield result
    finally:
        rmtree(str(result.project))


@pytest.fixture
def baked_in_temp_dir(cookies, request):
    """
    Delete the temporal directory that is created when executing the tests
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
