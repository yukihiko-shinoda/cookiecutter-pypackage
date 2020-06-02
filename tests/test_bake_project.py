"""Implements tests."""
import datetime
import importlib
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from subprocess import PIPE
from typing import List

import pytest  # type: ignore
from click.testing import CliRunner
from cookiecutter.utils import rmtree  # type: ignore
from pytest_cookies.plugin import Result  # type: ignore


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_subrocess(command):
    try:
        subprocess.run(shlex.split(command), check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as error:
        print(error.output)
        raise error


def run_inside_dir(commands, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param commands: Commands that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        for command in commands:
            run_subrocess(command)


def test_year_compute_in_license_file(baked_in_temp_dir):
    """License file should contains year string."""
    license_file_path = baked_in_temp_dir.project.join("LICENSE")
    now = datetime.datetime.now()
    assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1].replace("-", "")
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(baked_in_temp_dir):
    """Baked project should have specific files and directories."""
    assert baked_in_temp_dir.project.isdir()
    assert baked_in_temp_dir.exit_code == 0
    assert baked_in_temp_dir.exception is None
    check_toplevel_path_exist(
        baked_in_temp_dir, ["setup.py", "pythonboilerplate", "tests"]
    )


def check_toplevel_path_exist(result: Result, list_path: List[str]):
    found_toplevel_files = list_files(result)
    for path in list_path:
        assert path in found_toplevel_files


def test_bake_and_run_tests(baked_in_temp_dir):
    assert baked_in_temp_dir.project.isdir()
    run_inside_dir(["python setup.py test"], str(baked_in_temp_dir.project))
    print("test_bake_and_run_tests path", str(baked_in_temp_dir.project))


@pytest.mark.parametrize(
    "baked_in_temp_dir",
    [{"full_name": 'name "quote" name'}],
    indirect=["baked_in_temp_dir"],
)
def test_bake_withspecialchars_and_run_tests(baked_in_temp_dir):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    assert baked_in_temp_dir.project.isdir()
    run_inside_dir(["python setup.py test"], str(baked_in_temp_dir.project))


@pytest.mark.parametrize(
    "baked_in_temp_dir", [{"full_name": "O'connor"}], indirect=["baked_in_temp_dir"],
)
def test_bake_with_apostrophe_and_run_tests(baked_in_temp_dir):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    assert baked_in_temp_dir.project.isdir()
    run_inside_dir(["python setup.py test"], str(baked_in_temp_dir.project))


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
def test_bake_without_travis_pypi_setup(baked_in_temp_dir):
    assert not (
        baked_in_temp_dir.project / Path(".github/workflows/deploy.yml")
    ).exists()


def list_files(result: Result, directories: List[str] = None):
    directories = [] if directories is None else directories
    joined_path = result.project
    for directory in directories:
        joined_path = joined_path.join(directory)
    return [f.basename for f in joined_path.listdir()]


def read_text(result: Result, relative_path):
    return Path(str(result.project.join(relative_path))).read_text()


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
    resource_path_root, baked_in_temp_dir, license_trove_classifier, file_name_expected,
):
    """
    Source of expected text file:
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
    assert license_trove_classifier in baked_in_temp_dir.project.join("setup.py").read()
    actual_license_file = baked_in_temp_dir.project.join("LICENSE")
    expect_license_file = resource_path_root / "license" / (file_name_expected + ".txt")
    current_year = str(datetime.datetime.now().year)
    actual_license_text = actual_license_file.read().replace("\r\n", "\n")
    expect_license_text = expect_license_file.read_text().replace("2020", current_year)
    assert actual_license_text == expect_license_text
    assert not Path(str(baked_in_temp_dir.project.join("licenses"))).exists()


@pytest.mark.parametrize(
    "baked_in_temp_dir",
    [{"open_source_license": "Not open source"}],
    indirect=["baked_in_temp_dir"],
)
def test_bake_not_open_source(baked_in_temp_dir):
    found_toplevel_files = [f.basename for f in baked_in_temp_dir.project.listdir()]
    assert "setup.py" in found_toplevel_files
    assert "LICENSE" not in found_toplevel_files


@pytest.mark.parametrize(
    "baked_in_temp_dir, list_expected, list_not_expected",
    [
        ({"use_pyup": "n", "open_source_license": "MIT",}, [], ["[![Updates]("]),
        (
            {"use_pyup": "n", "open_source_license": "Not open source",},
            [],
            ["[![Updates]("],
        ),
        ({"use_pyup": "y", "open_source_license": "MIT",}, ["[![Updates]("], []),
        (
            {"use_pyup": "y", "open_source_license": "Not open source",},
            ["[![Updates]("],
            [],
        ),
    ],
    indirect=["baked_in_temp_dir"],
)
def test_bake_readme(baked_in_temp_dir, list_expected, list_not_expected):
    """README.md should have appropriate badges."""
    string_readme = baked_in_temp_dir.project.join("README.md").read()
    print(string_readme)
    for expected in list_expected:
        assert expected in string_readme
    for not_expected in list_not_expected:
        assert not_expected not in string_readme


def test_using_pytest(baked_in_temp_dir):
    """
    Pipfile should contain pytest.
    First test python file should import pytest.
    Command "python setup.py pytest" should work.
    Command "python setup.py test" should work.
    """
    assert baked_in_temp_dir.project.isdir()
    # Test Pipfile installs pytest
    assert pytest_entry_exists_in_pipfile(baked_in_temp_dir)
    # Test conftest.py exist
    assert conftest_exists(baked_in_temp_dir)
    # Test contents of test file
    check_is_pytest(get_test_file_text(baked_in_temp_dir))
    # Test the new pytest target
    run_inside_dir(["python setup.py pytest"], str(baked_in_temp_dir.project))
    # Test the test alias (which invokes pytest)
    run_inside_dir(["python setup.py test"], str(baked_in_temp_dir.project))


@pytest.mark.parametrize(
    "baked_in_temp_dir", [{"use_pytest": "n"}], indirect=["baked_in_temp_dir"],
)
def test_not_using_pytest(baked_in_temp_dir):
    """
    Pipfile should not contain pytest.
    First test python file should import unittest.
    First test python file should not import pytest.
    """
    assert baked_in_temp_dir.project.isdir()
    # Test Pipfile doesn install pytest
    assert not pytest_entry_exists_in_pipfile(baked_in_temp_dir)
    # Test conftest.py not exist
    assert not conftest_exists(baked_in_temp_dir)
    # Test contents of test file
    test_file = get_test_file_text(baked_in_temp_dir)
    check_is_unittest(get_test_file_text(baked_in_temp_dir))


def check_is_pytest(test_file):
    assert "import unittest" not in test_file
    assert "def test_content(response):" in test_file


def check_is_unittest(test_file):
    assert "import unittest" in test_file
    assert "def test_content(response):" not in test_file


def conftest_exists(baked_in_temp_dir):
    return (baked_in_temp_dir.project / Path("tests/conftest.py")).exists()


def get_test_file_text(baked_in_temp_dir):
    return Path(
        str(baked_in_temp_dir.project.join("tests/test_pythonboilerplate.py"))
    ).read_text()


def pytest_entry_exists_in_pipfile(result):
    pipfile_file_path = result.project.join("Pipfile")
    lines = pipfile_file_path.readlines()
    return 'pytest = "*"\n' in lines


# def test_project_with_hyphen_in_module_name(cookies):
#     result = cookies.bake(
#         extra_context={'project_name': 'something-with-a-dash'}
#     )
#     assert result.project is not None
#     project_path = str(result.project)
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


def test_bake_with_no_console_script(cookies):
    """
    There should be no cli.py file.
    setup.py should not have entry_points.
    """
    context = {"command_line_interface": "No command-line interface"}
    result = cookies.bake(extra_context=context)
    project_path, _project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" not in found_project_files

    setup_path = os.path.join(project_path, "setup.py")
    with open(setup_path, "r") as setup_file:
        assert "entry_points" not in setup_file.read()


def test_bake_with_console_script_files(cookies):
    check_bake_with_console_script_files("click", cookies)


def test_bake_with_argparse_console_script_files(cookies):
    check_bake_with_console_script_files("argparse", cookies)


def check_bake_with_console_script_files(cli, cookies):
    """
    There should be cli.py file.
    setup.py should have entry_points.
    """
    context = {"command_line_interface": cli}
    result = cookies.bake(extra_context=context)
    project_path, _project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files
    setup_path = os.path.join(project_path, "setup.py")
    with open(setup_path, "r") as setup_file:
        assert "entry_points" in setup_file.read()


def test_bake_with_console_script_cli(cookies):
    check_bake_with_console_script_cli("click", cookies)


def test_bake_with_argparse_console_script_cli(cookies):
    check_bake_with_console_script_cli("argparse", cookies)


def check_bake_with_console_script_cli(command_line_interface, cookies):
    """Command line output should includes appropriate string."""
    context = {"command_line_interface": command_line_interface}
    result = cookies.bake(extra_context=context)
    _project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, "cli.py")
    module_name = ".".join([project_slug, "cli"])
    # noinspection PyUnresolvedReferences
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    # noinspection PyUnresolvedReferences
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    runner = CliRunner()
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = " ".join(
        ["Replace this message by putting your code into", project_slug]
    )
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output


def test_bake_and_run_invoke_tests(baked_in_temp_dir):
    """Run the unit tests of a newly-generated project"""
    assert baked_in_temp_dir.project.isdir()
    run_inside_dir(
        ["pip install pipenv", "pipenv install --dev", "pipenv run invoke test"],
        str(baked_in_temp_dir.project),
    )


def test_bake_and_run_invoke_style(baked_in_temp_dir):
    """Run the formatter on a newly-generated project"""
    if (
        sys.version_info.major <= 2
        or sys.version_info.major == 3
        and sys.version_info.major <= 5
    ):
        return
    assert baked_in_temp_dir.project.isdir()
    run_inside_dir(
        [
            "pip install pipenv",
            "pipenv install --dev",
            "pipenv run invoke style --check",
        ],
        str(baked_in_temp_dir.project),
    )


def test_bake_and_run_invoke_lint(baked_in_temp_dir):
    """Run the linter on a newly-generated project"""
    assert baked_in_temp_dir.project.isdir()
    run_inside_dir(
        ["pip install pipenv", "pipenv install --dev", "pipenv run invoke lint"],
        str(baked_in_temp_dir.project),
    )


def test_bake_and_run_invoke_coverage(baked_in_temp_dir):
    """Run the linter on a newly-generated project"""
    assert baked_in_temp_dir.project.isdir()
    run_inside_dir(
        [
            "pip install pipenv",
            "pipenv install --dev",
            "pipenv run invoke coverage --xml",
        ],
        str(baked_in_temp_dir.project),
    )
