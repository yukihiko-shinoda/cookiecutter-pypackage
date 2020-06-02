# {{ cookiecutter.project_name }}

[![Test](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repository_name }}/workflows/Test/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repository_name }}/actions?query=workflow%3ATest)
[![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repository_name }})](https://codeclimate.com/github/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repository_name }})
{% if cookiecutter.use_pyup != 'n' -%}
[![Updates](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repository_name }}/shield.svg)](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repository_name }}/)
{% endif -%}
[![Python versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug }})
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2F{{ cookiecutter.github_username }}%2F{{ cookiecutter.github_repository_name }})](http://twitter.com/share?text={{ cookiecutter.project_name | urlencode }}&url=https://pypi.org/project/{{ cookiecutter.project_slug }}/&hashtags=python)

{{ cookiecutter.project_short_description }}

## Features

* TODO

## Credits

This package was created with [Cookiecutter] and the [yukihiko-shinoda/cookiecutter-pypackage] project template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[yukihiko-shinoda/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
