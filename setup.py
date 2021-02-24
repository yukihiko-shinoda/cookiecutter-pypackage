# !/usr/bin/env python
"""The setup script."""

from distutils.core import setup

setup(
    name="cookiecutter-pypackage",
    packages=[],
    version="0.2.0",
    description="Cookiecutter template for a Python package",
    author="Sam Briggs",
    license="BSD",
    author_email="briggySmalls90@gmail.com",
    url="https://github.com/briggySmalls/cookiecutter-pypackage",
    keywords=["cookiecutter", "template", "package"],
    python_requires=">=3.5",
    install_requires=["cookiecutter"],
    dependency_links=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
    ],
)
