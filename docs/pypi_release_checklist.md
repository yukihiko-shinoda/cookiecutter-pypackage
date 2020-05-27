# PyPI Release Checklist

## Before Your First Release

1\. Register the package on PyPI:

```console
python setup.py register
```

2\. Visit PyPI to make sure it registered.

## For Every Release

1\. Commit the changes:

```console
git commit -m "Changelog for upcoming release 0.1.1."
```

2\. Update version number (can also be patch or major)

```console
bump2version minor
```

3\. Push the commit:

```console
git push
```

4\. Check test result at GitHub Actions

5\. Push the tags, creating the new release on both GitHub and PyPI:

```console
git push --tags
```

6\. Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, try one of these:

6-1\. Check your long_description locally:

```console
pip install readme_renderer
python setup.py check -r -s
```

## About This Checklist

This checklist is arranged from:

- [https://gist.github.com/audreyr/5990987](https://gist.github.com/audreyr/5990987)
- [https://gist.github.com/audreyr/9f1564ea049c14f682f4](https://gist.github.com/audreyr/9f1564ea049c14f682f4)

It assumes that you are using all features of Cookiecutter PyPackage.
