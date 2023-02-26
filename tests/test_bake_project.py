"""Implements tests."""
from contextlib import contextmanager
import datetime
import importlib
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
import os
from pathlib import Path
import shlex
import subprocess
from subprocess import PIPE
import sys
from textwrap import dedent
from traceback import TracebackException
from types import ModuleType
from typing import Any, Generator, List, Optional, Tuple

from click.testing import CliRunner
import pytest
from pytest import CaptureFixture
from pytest_cookies.plugin import Cookies, Result
from pytest_mock import MockerFixture

from tests.conftest import process_result
from tests.testlibraries.argparse_cli_runner import ArgparseCliRunner

WARNING_FOR_PYTHON_35 = (
    b"DEPRECATION: Python 3.5 reached the end of its life on September 13th, 2020."
    b" Please upgrade your Python as Python 3"
)


@contextmanager
def inside_dir(dirpath: str) -> Generator[None, None, None]:
    """Execute code from inside the given directory.

    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(
    cookies: Cookies, *args: Any, **kwargs: Any
) -> Generator[Result, None, None]:
    """Delete the temporal directory that is created when executing the tests.

    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    yield from process_result(result)


def run_subrocess(command: str) -> None:
    try:
        subprocess.run(shlex.split(command), check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as error:
        print(str(error.stdout).encode("ascii", "ignore").decode("unicode_escape"))
        print(str(error.stderr).encode("ascii", "ignore").decode("unicode_escape"))
        raise


def run_inside_dir(commands: List[str], dirpath: str) -> None:
    """Run a command from inside a given directory, returning the exit status.

    :param commands: Commands that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        try:
            for command in commands:
                run_subrocess(command)
        except subprocess.CalledProcessError:
            print((Path(dirpath) / "pyproject.toml").read_text())
            raise


def test_year_compute_in_license_file(baked_in_temp_dir: Result) -> None:
    """License file should contains year string."""
    license_file_path = baked_in_temp_dir.project_path / "LICENSE"
    now = datetime.datetime.now()
    assert str(now.year) in license_file_path.read_text()


def project_info(result: Result) -> Tuple[Optional[Path], str, Path]:
    """Get toplevel dir, project_slug, and project dir from baked cookies."""
    project_path = result.project_path
    project_slug = os.path.split(project_path)[-1].replace("-", "")
    project_dir = project_path / project_slug
    return project_path, project_slug, project_dir


def test_bake_with_defaults(baked_in_temp_dir: Result) -> None:
    """Baked project should have specific files and directories."""
    assert baked_in_temp_dir.project_path.is_dir()
    assert baked_in_temp_dir.exit_code == 0
    assert baked_in_temp_dir.exception is None
    check_toplevel_path_exist(
        baked_in_temp_dir, ["setup.py", "pythonboilerplate", "tests"]
    )


def check_toplevel_path_exist(result: Result, list_path: List[str]) -> None:
    found_toplevel_files = list_files(result)
    for path in list_path:
        assert path in found_toplevel_files


def test_bake_and_run_tests(baked_in_temp_dir: Result) -> None:
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir_python_setup_py_test(baked_in_temp_dir)
    print("test_bake_and_run_tests path", str(baked_in_temp_dir.project_path))


@pytest.mark.parametrize(
    "baked_in_temp_dir",
    [{"full_name": 'name "quote" name'}],
    indirect=["baked_in_temp_dir"],
)
def test_bake_withspecialchars_and_run_tests(baked_in_temp_dir: Result) -> None:
    """Ensure that a `full_name` with double quotes does not break setup.py."""
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir_python_setup_py_test(baked_in_temp_dir)


@pytest.mark.parametrize(
    "baked_in_temp_dir", [{"full_name": "O'connor"}], indirect=["baked_in_temp_dir"]
)
def test_bake_with_apostrophe_and_run_tests(baked_in_temp_dir: Result) -> None:
    """Ensure that a `full_name` with apostrophes does not break setup.py."""
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir_python_setup_py_test(baked_in_temp_dir)


# def test_bake_and_run_travis_pypi_setup(cookies):
#     # given:
#     with bake_in_temp_dir(cookies) as result:
#         project_path = str(result.project)
#
#         # when:
#         travis_setup_cmd = ('python travis_pypi_setup.py'
#                             ' --repo audreyr/cookiecutter-pypackage'
#                             ' --password invalidpass')
#         run_inside_dir(travis_setup_cmd, project_path)
#         # then:
#         result_travis_config = yaml.load(
#             result.project.join(".travis.yml").open()
#         )
#         min_size_of_encrypted_password = 50
#         assert len(
#             result_travis_config["deploy"]["password"]["secure"]
#         ) > min_size_of_encrypted_password


@pytest.mark.parametrize(
    "baked_in_temp_dir",
    [{"use_pypi_deployment_with_github_actions": "n"}],
    indirect=["baked_in_temp_dir"],
)
def test_bake_without_travis_pypi_setup(baked_in_temp_dir: Result) -> None:
    assert not (
        baked_in_temp_dir.project_path / Path(".github/workflows/deploy.yml")
    ).exists()


def list_files(result: Result, directories: Optional[List[str]] = None) -> List[str]:
    directories = [] if directories is None else directories
    joined_path = result.project_path
    for directory in directories:
        joined_path = str(joined_path / directory)
    return [f.name for f in joined_path.iterdir()]


@pytest.mark.parametrize(
    "baked_in_temp_dir, license_trove_classifier, file_name_expected",
    [
        (
            {"open_source_license": "MIT"},
            "License :: OSI Approved :: MIT License",
            "mit",
        ),
        (
            {"open_source_license": "GPL-3.0-or-later"},
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "gpl3.0_github",
        ),
        (
            {"open_source_license": "Apache-2.0"},
            "License :: OSI Approved :: Apache Software License",
            "apache2.0_github",
        ),
        (
            {"open_source_license": "BSD-3-Clause"},
            "License :: OSI Approved :: BSD License",
            "bsd3clause",
        ),
        (
            {"open_source_license": "GPL-3.0-or-later-short"},
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "gpl3.0_gnu",
        ),
        (
            {"open_source_license": "Apache-2.0-short"},
            "License :: OSI Approved :: Apache Software License",
            "apache2.0_apache",
        ),
    ],
    indirect=["baked_in_temp_dir"],
)
def test_bake_selecting_license(
    resource_path_root: Path,
    baked_in_temp_dir: Result,
    license_trove_classifier: str,
    file_name_expected: str,
) -> None:
    """Source of expected text file:

    - mit.txt: Exported from GitHub
    - gpl3.0_gnu.txt:
      @see https://www.gnu.org/licenses/gpl-3.0.en.html
      "How to Apply These Terms to Your New Programs"
      GitHub doesn't recognize.
    - apache2.0_apache.txt:
      @see https://www.apache.org/licenses/LICENSE-2.0#apply
      GitHub doesn't recognize.
    - bsd3clause.txt: Exported from GitHub
    """
    assert (
        license_trove_classifier
        in (baked_in_temp_dir.project_path / "pyproject.toml").read_text()
    )
    actual_license_file = baked_in_temp_dir.project_path / "LICENSE"
    expect_license_file = resource_path_root / "license" / (file_name_expected + ".txt")
    current_year = str(datetime.datetime.now().year)
    actual_license_text = actual_license_file.read_text().replace("\r\n", "\n")
    expect_license_text = expect_license_file.read_text().replace("2020", current_year)
    assert actual_license_text == expect_license_text
    assert not (baked_in_temp_dir.project_path / "licenses").exists()


@pytest.mark.parametrize(
    "baked_in_temp_dir",
    [{"open_source_license": "Not open source"}],
    indirect=["baked_in_temp_dir"],
)
def test_bake_not_open_source(baked_in_temp_dir: Result) -> None:
    """Project not open source license should not have file: "LICENSE"."""
    found_toplevel_files = [f.name for f in baked_in_temp_dir.project_path.iterdir()]
    assert "setup.py" in found_toplevel_files
    assert "LICENSE" not in found_toplevel_files


@pytest.mark.parametrize(
    "baked_in_temp_dir, list_expected, list_not_expected",
    [
        ({"use_pyup": "n", "open_source_license": "MIT"}, [], ["[![Updates]("]),
        (
            {"use_pyup": "n", "open_source_license": "Not open source"},
            [],
            ["[![Updates]("],
        ),
        ({"use_pyup": "y", "open_source_license": "MIT"}, ["[![Updates]("], []),
        (
            {"use_pyup": "y", "open_source_license": "Not open source"},
            ["[![Updates]("],
            [],
        ),
    ],
    indirect=["baked_in_temp_dir"],
)
def test_bake_readme(
    baked_in_temp_dir: Result, list_expected: List[str], list_not_expected: List[str]
) -> None:
    """README.md should have appropriate badges."""
    string_readme = (baked_in_temp_dir.project_path / "README.md").read_text()
    for expected in list_expected:
        assert expected in string_readme
    for not_expected in list_not_expected:
        assert not_expected not in string_readme


def test_using_pytest(baked_in_temp_dir: Result) -> None:
    """Pipfile should contain pytest.

    First test python file should import pytest. Command "python setup.py pytest" should
    work. Command "python setup.py test" should work.
    """
    assert baked_in_temp_dir.project_path.is_dir()
    # Test Pipfile installs pytest
    assert pytest_entry_exists_in_pipfile(baked_in_temp_dir)
    # Test conftest.py exist
    assert conftest_exists(baked_in_temp_dir)
    # Test contents of test file
    check_is_pytest(get_test_file_text(baked_in_temp_dir))
    # Test the new pytest target
    run_inside_dir_python_setup_py_pytest(baked_in_temp_dir)
    # Test the test alias (which invokes pytest)
    run_inside_dir_python_setup_py_test(baked_in_temp_dir)


def run_inside_dir_python_setup_py_test(baked_in_temp_dir: Result) -> None:
    try:
        run_inside_dir(["pytest"], str(baked_in_temp_dir.project_path))
    except subprocess.CalledProcessError as error:
        if error.stderr.find(WARNING_FOR_PYTHON_35) == -1:
            raise error


def run_inside_dir_python_setup_py_pytest(baked_in_temp_dir: Result) -> None:
    try:
        run_inside_dir(["pytest"], str(baked_in_temp_dir.project_path))
    except subprocess.CalledProcessError as error:
        if error.stderr.find(WARNING_FOR_PYTHON_35) == -1:
            raise error


@pytest.mark.parametrize(
    "baked_in_temp_dir", [{"use_pytest": "n"}], indirect=["baked_in_temp_dir"]
)
def test_not_using_pytest(baked_in_temp_dir: Result) -> None:
    """Pipfile should not contain pytest.

    First test python file should import unittest. First test python file should not
    import pytest.
    """
    assert baked_in_temp_dir.project_path.is_dir()
    # Test Pipfile doesn install pytest
    assert not pytest_entry_exists_in_pipfile(baked_in_temp_dir)
    # Test conftest.py not exist
    assert not conftest_exists(baked_in_temp_dir)
    # Test contents of test file
    check_is_unittest(get_test_file_text(baked_in_temp_dir))


def check_is_pytest(test_file: str) -> None:
    assert "import unittest" not in test_file
    assert "def test_content(response):" in test_file


def check_is_unittest(test_file: str) -> None:
    assert "import unittest" in test_file
    assert "def test_content(response):" not in test_file


def conftest_exists(baked_in_temp_dir: Result) -> bool:
    if not isinstance(baked_in_temp_dir.project_path, Path):
        raise ValueError(baked_in_temp_dir)
    return (baked_in_temp_dir.project_path / "tests/conftest.py").exists()


def get_test_file_text(baked_in_temp_dir: Result) -> str:
    if not isinstance(baked_in_temp_dir.project_path, Path):
        raise ValueError(baked_in_temp_dir)
    return (
        baked_in_temp_dir.project_path / "tests/test_pythonboilerplate.py"
    ).read_text("utf-8")


def pytest_entry_exists_in_pipfile(result: Result) -> bool:
    pipfile_file_path = result.project_path / "Pipfile"
    lines = pipfile_file_path.read_text().splitlines()
    return 'pytest = "*"' in lines


# def test_project_with_hyphen_in_module_name(cookies):
#     result = cookies.bake(
#         extra_context={'project_name': 'something-with-a-dash'}
#     )
#     assert result.project_path is not None
#     project_path = str(result.project_path)
#
#     # when:
#     travis_setup_cmd = ('python travis_pypi_setup.py'
#                         ' --repo audreyr/cookiecutter-pypackage'
#                         ' --password invalidpass')
#     run_inside_dir(travis_setup_cmd, project_path)
#
#     # then:
#     result_travis_config = yaml.load(
#         open(os.path.join(project_path, ".travis.yml"))
#     )
#     assert "secure" in result_travis_config["deploy"]["password"],\
#         "missing password config in .travis.yml"


def test_bake_with_no_console_script(cookies: Cookies) -> None:
    """There should be no cli.py file.

    setup.py should not have entry_points.
    """
    context = {"command_line_interface": "No command-line interface"}
    result = cookies.bake(extra_context=context)
    if result.exit_code:
        raise AssertionError(result.exception) from result.exception
    project_path, _project_slug, project_dir = project_info(result)
    found_project_files = Path.iterdir(project_dir)
    assert "cli.py" not in list(found_project_files)
    assert project_path is not None
    setup_path = os.path.join(project_path, "setup.py")
    with open(setup_path, "r", encoding="utf-8") as setup_file:
        assert "entry_points" not in setup_file.read()


def test_bake_with_console_script_files(cookies: Cookies) -> None:
    check_bake_with_console_script_files("Click", cookies)


def test_bake_with_argparse_console_script_files(cookies: Cookies) -> None:
    check_bake_with_console_script_files("Argparse", cookies)


def check_bake_with_console_script_files(cli: str, cookies: Cookies) -> None:
    """There should be cli.py file.

    setup.py should have entry_points.
    """
    context = {"command_line_interface": cli}
    result = cookies.bake(extra_context=context)
    if result.exit_code:
        raise AssertionError(result.exception) from result.exception
    project_path, _project_slug, project_dir = project_info(result)
    found_project_files = Path.iterdir(project_dir)
    assert "cli.py" in [f.name for f in found_project_files]
    if not isinstance(project_path, Path):
        raise ValueError(result)
    setup_path = os.path.join(project_path, "pyproject.toml")
    with open(setup_path, "r", encoding="utf-8") as setup_file:
        assert "[project.entry-points.console_scripts]" in setup_file.read()


def test_bake_with_console_script_cli(cookies: Cookies) -> None:
    check_bake_with_console_script_cli(
        "Click", cookies, CliRunner(), "Show this message"
    )


def test_bake_with_argparse_console_script_cli(
    cookies: Cookies, capsys: CaptureFixture[str], mocker: MockerFixture
) -> None:
    """Command line of argparse output should includes appropriate string."""
    help_message = dedent("-h, --help  show this help message and exit")
    check_bake_with_console_script_cli(
        "Argparse", cookies, ArgparseCliRunner(capsys, mocker), help_message
    )


def check_bake_with_console_script_cli(
    command_line_interface: str, cookies: Cookies, runner: CliRunner, help_message: str
) -> None:
    """Command line output should includes appropriate string."""
    context = {"command_line_interface": command_line_interface}
    result = cookies.bake(extra_context=context)
    if result.exit_code:
        raise AssertionError(result.exception) from result.exception
    _project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, "cli.py")
    module_name = ".".join([project_slug, "cli"])
    cli = create_module_type(module_name, module_path)
    check_noarg(runner, cli, project_slug)
    check_help(runner, cli, help_message)


def create_module_type(module_name: str, module_path: str) -> ModuleType:
    """Creates Module type to call it from Python code."""
    # noinspection PyUnresolvedReferences
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if not isinstance(spec, ModuleSpec):
        raise ValueError(module_name, module_path)
    # noinspection PyUnresolvedReferences
    module = importlib.util.module_from_spec(spec)
    if not isinstance(spec.loader, Loader):
        raise ValueError(spec, module)
    spec.loader.exec_module(module)
    return module


def check_noarg(runner: CliRunner, cli: ModuleType, project_slug: str) -> None:
    """Command line output should includes default message."""
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0, (
        noarg_result.stdout + noarg_result.stderr + ""
        if noarg_result.exception is None
        else "".join(TracebackException.from_exception(noarg_result.exception).format())
    )
    noarg_output = " ".join(
        ["Replace this message by putting your code into", project_slug]
    )
    assert noarg_output in noarg_result.output


def check_help(runner: CliRunner, cli: ModuleType, help_message: str) -> None:
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0, help_result.stdout + help_result.stderr
    assert help_message in help_result.output


@pytest.mark.slow
def test_bake_and_run_invoke_tests(baked_in_temp_dir: Result) -> None:
    """Run the unit tests of a newly-generated project."""
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir(
        ["pip install pipenv", "pipenv install --dev", "pipenv run invoke test"],
        str(baked_in_temp_dir.project_path),
    )


@pytest.mark.slow
@pytest.mark.skipif(sys.version_info < (3, 7), reason="The black doesn't support.")
def test_bake_and_run_invoke_style(baked_in_temp_dir: Result) -> None:
    """Run the formatter on a newly-generated project."""
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir(
        [
            "pip install pipenv",
            "pipenv install --dev",
            "pipenv run invoke style --check",
        ],
        str(baked_in_temp_dir.project_path),
    )


@pytest.mark.slow
def test_bake_and_run_invoke_lint(baked_in_temp_dir: Result) -> None:
    """Run the linter on a newly-generated project."""
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir(
        ["pip install pipenv", "pipenv install --dev", "pipenv run invoke lint"],
        str(baked_in_temp_dir.project_path),
    )


@pytest.mark.slow
def test_bake_and_run_invoke_coverage(baked_in_temp_dir: Result) -> None:
    """Run the linter on a newly-generated project."""
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir(
        [
            "pip install pipenv",
            "pipenv install --dev --verbose",
            "pipenv run invoke test.coverage --xml",
        ],
        str(baked_in_temp_dir.project_path),
    )


@pytest.mark.slow
def test_bake_and_run_pyvelocity(baked_in_temp_dir: Result) -> None:
    """Run the linter on a newly-generated project."""
    assert baked_in_temp_dir.project_path.is_dir()
    run_inside_dir(
        [
            "pip install pipenv",
            "pipenv install --dev --verbose",
            "pipenv run pyvelocity",
        ],
        str(baked_in_temp_dir.project_path),
    )
