#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
LICENSE_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "licenses")


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def prepare_license(key_license):
    license_file = {
        "MIT": "mit.txt",
        "GPL-3.0-or-later": "gpl3.0_github.txt",
        "Apache-2.0": "apache2.0_github.txt",
        "BSD-3-Clause": "bsd3clause.txt",
        "GPL-3.0-or-later-short": "gpl3.0_gnu.txt",
        "Apache-2.0-short": "apache2.0_apache.txt",
    }.get(key_license)
    shutil.copy(
        os.path.join(LICENSE_DIRECTORY, license_file),
        os.path.join(PROJECT_DIRECTORY, "LICENSE"),
    )


if __name__ == "__main__":
    if "{{ cookiecutter.use_pypi_deployment_with_github_actions }}" != "y":
        remove_file(".github/workflows/deploy.yml")
    if "{{ cookiecutter.use_pyup }}" == "n":
        remove_file(".pyup.yml")
    if "no" in "{{ cookiecutter.command_line_interface|lower }}":
        cli_file = os.path.join("{{ cookiecutter.project_slug }}", "cli.py")
        remove_file(cli_file)
    if "Not open source" != "{{ cookiecutter.open_source_license }}":
        prepare_license("{{ cookiecutter.open_source_license }}")
    shutil.rmtree(LICENSE_DIRECTORY)
