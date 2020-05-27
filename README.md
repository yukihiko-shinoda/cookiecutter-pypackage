# Cookiecutter PyPackage

[![Build Status](https://travis-ci.org/briggySmalls/cookiecutter-pypackage.svg?branch=master)](https://travis-ci.org/briggySmalls/cookiecutter-pypackage)

[Cookiecutter] template for a Python package, forked from [audreyr/cookiecutter-pypackage].

- GitHub repo: [https://github.com/briggySmalls/cookiecutter-pypackage/](https://github.com/briggySmalls/cookiecutter-pypackage/)
- Documentation: [https://briggysmalls.github.io/cookiecutter-pypackage/](https://briggysmalls.github.io/cookiecutter-pypackage/)
- Free software: BSD license

## Features

This template has all of the features of the original [audreyr/cookiecutter-pypackage], plus the following:

- Dependency tracking using [pipenv]
- Linting provided by both [pylint] and [flake8] [executed by Tox]
- Formatting provided by [yapf] and [isort] [checked by Tox]
- Autodoc your code from Google docstring style (optional)
- All development tasks (lint, format, test, etc) wrapped up in a python CLI by [invoke]

## Build Status

Linux:

[![Linux build status on Travis CI](https://img.shields.io/travis/briggySmalls/cookiecutter-pypackage.svg)](https://travis-ci.org/briggySmalls/cookiecutter-pypackage)

Windows:

[![Windows build status on Appveyor](https://ci.appveyor.com/api/projects/status/github/briggySmalls/cookiecutter-pypackage?branch=master&svg=true)](https://ci.appveyor.com/project/briggySmalls/cookiecutter-pypackage/branch/master)

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher):

```console
pip install -U cookiecutter
```

Generate a Python package project:

```console
cookiecutter https://github.com/briggySmalls/cookiecutter-pypackage.git
```

Then:

- Create a repo and put it there.
- Add the repo to your [Travis-CI] account.
- Install the dev requirements into a virtualenv. (`pipenv install --dev`)
- [Register] your project with PyPI.
- Run the Travis CLI command `travis encrypt --add deploy.password` to encrypt your PyPI password in Travis config
  and activate automated deployment on PyPI when you push a new tag to master branch.
- Add the repo to your [Read the Docs] account + turn on the Read the Docs service hook.
- Release your package by pushing a new tag to master.
- Get your code on! 😎 Add your package dependencies to your setup.py as you go, and lock them into your virtual environment with `pipenv install`.
- Activate your project on [pyup.io].

For more details, see the [cookiecutter-pypackage tutorial].

[audreyr/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[invoke]: http://www.pyinvoke.org/
[isort]: https://pypi.org/project/isort/
[yapf]: https://github.com/google/yapf
[flake8]: https://pypi.org/project/flake8/
[pylint]: https://www.pylint.org/
[pipenv]: https://pipenv.readthedocs.io/en/latest/
[original_pypackage]: https://github.com/briggySmalls/cookiecutter-pypackage/
[Travis-CI]: http://travis-ci.org/
[Tox]: http://testrun.org/tox/
[Sphinx]: http://sphinx-doc.org/
[Read the Docs]: https://readthedocs.io/
[pyup.io]: https://pyup.io/
[bump2version]: https://github.com/c4urself/bump2version
[Punch]: https://github.com/lgiordani/punch
[Pipenv]: https://pipenv.readthedocs.io/en/latest/
[PyPi]: https://pypi.python.org/pypi
[pip docs for requirements files]: https://pip.pypa.io/en/stable/user_guide/#requirements-files
[Register]: https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives
[cookiecutter-pypackage tutorial]: https://briggysmalls.github.io/cookiecutter-pypackage/tutorial.html
