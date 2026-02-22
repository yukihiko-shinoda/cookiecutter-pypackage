# Cookiecutter PyPackage

[![Test](https://github.com/yukihiko-shinoda/cookiecutter-pypackage/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/cookiecutter-pypackage/actions?query=workflow%3ATest)
[![Maintainability](https://qlty.sh/gh/yukihiko-shinoda/projects/cookiecutter-pypackage/maintainability.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/cookiecutter-pypackage)
[![Code Coverage](https://qlty.sh/gh/yukihiko-shinoda/projects/cookiecutter-pypackage/coverage.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/cookiecutter-pypackage)

[Cookiecutter] template for a Python package, forked from [briggySmalls/cookiecutter-pypackage].

- Documentation: [https://yukihiko-shinoda.github.io/docs-cookiecutter-pypackage/](https://yukihiko-shinoda.github.io/docs-cookiecutter-pypackage/)

## Features

This template focus following:

- Target Python version: 3.7 - 3.13
- Dependency tracking using [uv]
- Linting provided by both [pylint], [flake8], [mypy] [executed by GitHub Actions]
- Formatting provided by [Ruff] [docformetter] [checked by GitHub Actions]
- Analyzing complexity and maintainability provided by [radon], [xenon] [checked by GitHub Actions]
- All development tasks (lint, format, analyze, test, etc) excluding deployment wrapped up in a python CLI by [invoke]
- Omit documentation workflows
  since this project targets early stages of development.
  In the early stages of development it is better to focus on providing
  working software and writing README.md than providing comprehensive
  documentation.

  @see [Manifesto for Agile Software Development](https://agilemanifesto.org/iso/en/manifesto.html)

## Quickstart

1\.

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher):

```console
pip install -U cookiecutter
```

2\.

Generate a Python package project:

```console
cookiecutter https://github.com/yukihiko-shinoda/cookiecutter-pypackage.git --checkout master-yukihiko-shinoda
```

Then, you will interactively prompt some choices of templated values,
for detail of templated values, see the [Prompts].

Then initialized project direcotry is created in current directory.

## Points to review after creating initialized project directory

1\.
Review support range if the one of your package is not Python 3.7 - 3.13

- .github/workflows/test.yml
- pyproject.toml
  - python_requires
  - classifiers
- docs/CONTRIBUTING.md -> Get Started! -> 5. oldest Python version

2\.

Pin wheel version in `pyproject.toml` and execute `uv lock`
if you prefer stability of deployment task.

## Remaining task after creating initialized project directory

1\.

Commit and push to GitHub repository.

2\.

Activate your created repository on [Qlty].

If you prefer, Enable \[Pull request comments\] and \[Pull request status updates\] from \[Repo Settings\] -> \[GitHub\]

Copy and paste badge from \[Repo Settings\] -> \[Badges\] to this README file.

2-1\.

Copy "TEST REPORTER ID" from \[Test Coverages\]

2-2\.

register copied TEST REPORTER ID into secret in your pushed GitHub repository
as name "CC_TEST_REPORTER_ID".

3\.

Issue API token at [PyPI] and register into secret of your GitHub repository
as name `pypi_password`

4\.

Create tag `v[0-9]+.[0-9]+.[0-9]+` and push to GitHub repository
to deploy into [PyPI].

Then, get your code on! 😎
Add your package dependencies to your `pyproject.toml` with `uv install`.

[briggySmalls/cookiecutter-pypackage]: https://github.com/briggySmalls/cookiecutter-pypackage
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[uv]: https://pypi.org/project/uv/
[Ruff]: https://pypi.org/project/ruff/
[docformetter]: https://pypi.org/project/docformatter/
[pylint]: https://www.pylint.org/
[flake8]: https://pypi.org/project/flake8/
[mypy]: http://mypy-lang.org/
[radon]: https://radon.readthedocs.io/en/latest/
[xenon]: https://pypi.org/project/xenon/
[invoke]: http://www.pyinvoke.org/
[Qlty]: https://qlty.sh/
[PyPi]: https://pypi.python.org/pypi
[Prompts]: docs/prompts.md
