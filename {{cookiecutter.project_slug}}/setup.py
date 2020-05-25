#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages  # type: ignore

with open("README.md") as readme_file:
    readme = readme_file.read()

{%- set license_classifiers = {
    'MIT': 'License :: OSI Approved :: MIT License',
    'GPL-3.0-or-later': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Apache-2.0': 'License :: OSI Approved :: Apache Software License',
    'BSD-3-Clause': 'License :: OSI Approved :: BSD License',
    'GPL-3.0-or-later-short': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Apache-2.0-short': 'License :: OSI Approved :: Apache Software License',
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email="{{ cookiecutter.email }}",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
{%- if cookiecutter.open_source_license in license_classifiers %}
        "{{ license_classifiers[cookiecutter.open_source_license] }}",
{%- endif %}
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="{{ cookiecutter.project_short_description }}",  # noqa: E501 pylint: disable=line-too-long
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        "console_scripts": [
            "{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main",
        ],
    },
    {%- endif %}
    install_requires=[{%- if cookiecutter.command_line_interface|lower == 'click' %}'Click>=7.0',{%- endif %} ],
    dependency_links=[],
{%- if cookiecutter.open_source_license not in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="{{ cookiecutter.project_slug }}",
    name="{{ cookiecutter.project_slug }}",
    packages=find_packages(include=["{{ cookiecutter.project_slug }}", "{{ cookiecutter.project_slug }}.*"]),
    setup_requires=[{%- if cookiecutter.use_pytest == 'y' %}'pytest-runner',{%- endif %} ],
    test_suite="tests",
    tests_require=[{%- if cookiecutter.use_pytest == 'y' %}'pytest>=3',{%- endif %} ],
    url="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.github_repository_name }}",
    version="{{ cookiecutter.version }}",
    zip_safe=False,
)
