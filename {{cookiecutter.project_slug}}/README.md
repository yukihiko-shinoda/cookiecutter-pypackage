# {{ cookiecutter.project_name }}
{% set is_open_source = cookiecutter.open_source_license != 'Not open source' %}
[![Test](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug | replace("_", "-") }}/workflows/Test/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug | replace("_", "-") }}/actions?query=workflow%3ATest)
{% if cookiecutter.use_pyup != 'n' -%}
[![Updates](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg)](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/)
{% endif -%}
[![Python versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug | replace("_", "-") }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug | replace("_", "-") }})
{% if is_open_source -%}
[![Documentation Status](https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest)](https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest)
{% endif -%}
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2F{{ cookiecutter.github_username }}%2F{{ cookiecutter.project_slug | replace("_", "-") }})](http://twitter.com/share?text={{ cookiecutter.project_name | urlencode }}&url=https://pypi.org/project/{{ cookiecutter.project_slug | replace("_", "-") }}/&hashtags=python)

{{ cookiecutter.project_short_description }}

{% if is_open_source -%}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.

{% endif -%}
## Features

* TODO

## Credits

This package was created with [Cookiecutter] and the [yukihiko-shinoda/cookiecutter-pypackage] project template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[yukihiko-shinoda/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
