# Prompts

When you create a package, you are prompted to enter these values.

## Templated Values

The following appear in various parts of your generated project.

**full_name**
:   Your full name.

**email**
:   Your email address.

**github_username**
:   Your GitHub username.

**project_name**
:   The name of your new Python package project.

    This is used in documentation,
    so spaces and any characters are fine here.

**github_repository_name**
:   The name of GitHub repository to push generated project.

    GitHub repository often seems to be named with "-".

**project_slug**
:   The namespace of your Python package.

    This should be Python import-friendly.
    Typically, it is the slugified version of projectname.
    It seems to be better to aboid to use "-" nor "_".

    - [PEP 8 -- Style Guide for Python Code | Python.org](https://www.python.org/dev/peps/pep-0008/#package-and-module-names)
    - [PEP 423 -- Naming conventions and recipes related to packaging | Python.org](https://www.python.org/dev/peps/pep-0423/#follow-pep-8-for-syntax-of-package-and-module-names)
    - [PEP 423 -- Naming conventions and recipes related to packaging | Python.org](https://www.python.org/dev/peps/pep-0423/#use-a-single-name)
    - [naming - Is it ok to use dashes in Python files when trying to import them? - Stack Overflow](https://stackoverflow.com/questions/761519/is-it-ok-to-use-dashes-in-python-files-when-trying-to-import-them)

**project_short_description**
:   A 1-sentence description of what your Python package does.

**pypi_username**
:   Your Python Package Index account username.

    The [PyPI] or Python Package Index is
    the official third-party software repository
    for the Python programming language.
    Python developers intend it to be a comprehensive catalog
    of all open source Python packages.

**version**
:   The starting version number of the package.

## Options

The following package configuration options set up different features for your project.

**use_pytest**
:   Wheter use pytest for testing or not.

    When not "y", progect will be generated to use unittest for testing.

**use_pypi_deployment_with_github_actions**
:   Whether use PyPI deployment with GitHub Actions.

**use_pyup**
:   Whether use [pyup.io] to keep Python dependencies secure, up-to-date, and compliant.

    [pyup.io] is a service that helps you to keep your requirements files up to date.
    It sends you automated pull requests
    whenever there's a new release for one of your dependencies.

**command_line_interface**
:   Whether to create a console script and witch package use for.

    Console script entry point will match the project_slug.

**open_source_license**
:   Note that "GPL-3.0-or-later-short" and "Apache-2.0-short" is not recognized by GitHub.

    If you are stranger around license, linked workflow will be your helps.
    [Choose an open source license | Choose a License](Choose an open source license | Choose a License)

**python_code_max_length_per_line**
:   Max length per line of Python code.

This value will be set configure files for each linter and formater.

**pylint_docstring_min_length**
:   Minimum line length for functions/classes that require docstrings, shorter ones are exempt.

    In the early stages of development
    it is better to focus on providing working software
    and writing README.md than providing comprehensive documentation.

[PyPI]: https://pypi.python.org/pypi
[pyup.io]: https://pyup.io/
