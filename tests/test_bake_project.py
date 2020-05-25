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


def test_year_compute_in_license_file(cookies):
    """License file should contains year string."""
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    """Baked project should have specific files and directories."""
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None
        check_toplevel_path_exist(
            result, ["setup.py", "python_boilerplate", "tox.ini", "tests"]
        )


def check_toplevel_path_exist(result: Result, list_path: List[str]):
    found_toplevel_files = list_files(result)
    for path in list_path:
        assert path in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir(["python setup.py test"], str(result.project))
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(
        cookies, extra_context={"full_name": 'name "quote" name'}
    ) as result:
        assert result.project.isdir()
        run_inside_dir(["python setup.py test"], str(result.project))


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project.isdir()
        run_inside_dir(["python setup.py test"], str(result.project))


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


def test_bake_without_travis_pypi_setup(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_pypi_deployment_with_github_actions": "n"}
    ) as result:
        assert not (result.project / Path(".github/workflows/deploy.yml")).exists()


def test_bake_without_author_file(cookies):
    """
    Author file should not be created.
    There should be no spaces in the toc tree.
    """
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        assert "AUTHORS.rst" not in list_files(result)
        assert "authors.rst" not in list_files(result, ["docs"])
        assert "contributing\n   history" in read_text(result, "docs/index.rst")
        assert "AUTHORS.rst" not in read_text(result, "MANIFEST.in")


def list_files(result: Result, directories: List[str] = None):
    directories = [] if directories is None else directories
    joined_path = result.project
    for directory in directories:
        joined_path = joined_path.join(directory)
    return [f.basename for f in joined_path.listdir()]


def read_text(result: Result, relative_path):
    return Path(str(result.project.join(relative_path))).read_text()


@pytest.mark.parametrize(
    "key_license, license_trove_classifier, file_name_expected",
    [
        ("MIT", "License :: OSI Approved :: MIT License", "mit"),
        (
            "GPL-3.0-or-later",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "gpl3.0_github",
        ),
        (
            "Apache-2.0",
            "License :: OSI Approved :: Apache Software License",
            "apache2.0_github",
        ),
        ("BSD-3-Clause", "License :: OSI Approved :: BSD License", "bsd3clause",),
        (
            "GPL-3.0-or-later-short",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "gpl3.0_gnu",
        ),
        (
            "Apache-2.0-short",
            "License :: OSI Approved :: Apache Software License",
            "apache2.0_apache",
        ),
    ],
)
def test_bake_selecting_license(
    cookies,
    resource_path_root,
    key_license,
    license_trove_classifier,
    file_name_expected,
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
    with bake_in_temp_dir(
        cookies, extra_context={"open_source_license": key_license}
    ) as result:
        assert license_trove_classifier in result.project.join("setup.py").read()
        actual_license_file = result.project.join("LICENSE")
        expect_license_file = (
            resource_path_root / "license" / (file_name_expected + ".txt")
        )
        current_year = str(datetime.datetime.now().year)
        actual_license_text = actual_license_file.read().replace("\r\n", "\n")
        expect_license_text = expect_license_file.read_text().replace(
            "2020", current_year
        )
        assert actual_license_text == expect_license_text
        assert not Path(str(result.project.join("licenses"))).exists()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"open_source_license": "Not open source"}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files


@pytest.mark.parametrize(
    "use_pyup, open_source_license, list_expected, list_not_expected",
    [
        ("n", "MIT", ["[![Documentation Status](http"], ["[![Updates]("]),
        ("n", "Not open source", [], ["[![Documentation Status](http", "[![Updates]("]),
        ("y", "MIT", ["[![Documentation Status](http", "[![Updates]("], []),
        ("y", "Not open source", ["[![Updates]("], ["[![Documentation Status](http"]),
    ],
)
def test_bake_readme(
    cookies, use_pyup, open_source_license, list_expected, list_not_expected
):
    """README.md should have appropriate badges."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "use_pyup": use_pyup,
            "open_source_license": open_source_license,
        },
    ) as result:
        string_readme = result.project.join("README.md").read()
        print(string_readme)
        for expected in list_expected:
            assert expected in string_readme
        for not_expected in list_not_expected:
            assert not_expected not in string_readme


def test_using_pytest(cookies):
    """
    Pipfile should contain pytest.
    First test python file should import pytest.
    Command "python setup.py pytest" should work.
    Command "python setup.py test" should work.
    """
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        # Test Pipfile installs pytest
        pipfile_file_path = result.project.join("Pipfile")
        lines = pipfile_file_path.readlines()
        assert 'pytest = "*"\n' in lines
        # Test contents of test file
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        # Test the new pytest target
        run_inside_dir(["python setup.py pytest"], str(result.project))
        # Test the test alias (which invokes pytest)
        run_inside_dir(["python setup.py test"], str(result.project))


def test_not_using_pytest(cookies):
    """
    Pipfile should not contain pytest.
    First test python file should import unittest.
    First test python file should not import pytest.
    """
    with bake_in_temp_dir(cookies, extra_context={"use_pytest": "n"}) as result:
        assert result.project.isdir()
        # Test Pipfile doesn install pytest
        pipfile_file_path = result.project.join("Pipfile")
        lines = pipfile_file_path.readlines()
        assert 'pytest = "*"\n' not in lines
        # Test contents of test file
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import unittest" in "".join(lines)
        assert "import pytest" not in "".join(lines)


def test_using_google_docstrings(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        # Test docs include sphinx extension
        docs_conf_file_path = result.project.join("docs/conf.py")
        lines = docs_conf_file_path.readlines()
        assert "sphinx.ext.napoleon" in "".join(lines)


def test_not_using_google_docstrings(cookies):
    """conf.py should have string "sphinx.ext.napoleon"."""
    with bake_in_temp_dir(
        cookies, extra_context={"use_google_docstrings": "n"}
    ) as result:
        assert result.project.isdir()
        # Test docs do not include sphinx extension
        docs_conf_file_path = result.project.join("docs/conf.py")
        lines = docs_conf_file_path.readlines()
        assert "sphinx.ext.napoleon" not in "".join(lines)


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


def test_bake_and_run_invoke_tests(cookies):
    """Run the unit tests of a newly-generated project"""
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir(
            ["pip install pipenv", "pipenv install --dev", "pipenv run invoke test"],
            str(result.project),
        )


def test_bake_and_run_invoke_style(cookies):
    """Run the formatter on a newly-generated project"""
    if (
        sys.version_info.major <= 2
        or sys.version_info.major == 3
        and sys.version_info.major <= 5
    ):
        return
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir(
            [
                "pip install pipenv",
                "pipenv install --dev",
                "pipenv run invoke style --check",
            ],
            str(result.project),
        )


def test_bake_and_run_invoke_lint(cookies):
    """Run the linter on a newly-generated project"""
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir(
            ["pip install pipenv", "pipenv install --dev", "pipenv run invoke lint"],
            str(result.project),
        )


def test_bake_and_run_invoke_coverage(cookies):
    """Run the linter on a newly-generated project"""
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir(
            [
                "pip install pipenv",
                "pipenv install --dev",
                "pipenv run invoke coverage --xml",
            ],
            str(result.project),
        )
