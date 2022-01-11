<p align="center">
  <a href="https://codecov.io/gh/jalvaradosegura/version-checker">
    <img src="https://codecov.io/gh/jalvaradosegura/version-checker/branch/main/graph/badge.svg?token=GJMYL11SWF"/>
  </a>

  <a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="black">
  </a>

  <a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
  </a>

  <a href="https://github.com/jalvaradosegura/version-checker/actions/workflows/unit_tests.yml" target="_blank">
    <img src="https://github.com/jalvaradosegura/version-checker/actions/workflows/unit_tests.yml/badge.svg" alt="License">
  </a>

</p>

# version-checker
## Usage
### Config example
```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/jalvaradosegura/version-checker
    rev: v0.2.0-alpha
    hooks:
    -   id: version-checker
        args: [--files, CHANGELOG.md, Jenkinsfile, testing_hooks/__init__.py]
```
With this configuration we are saying: before each commit, check that the files defined after `--files`, contains the version indicated in the `pyproject.toml` file.

### How it looks when running it
Following the previous example, let's say that I updated the version of a package I'm working on to `3.0.0` in the `pyproject.toml` file. Then I updated almost all references to that version on the different files, but I forgot to do it on the `CHANGELOG.md` file:

<img src="https://i.imgur.com/q2ZuYV6.png" alt="Example">

If we then update the `CHANGELOG.md` file accordingly, the hook will pass.

> Remember that you can always set the `stages` parameter in your `.pre-commit-config.yaml`, to make it run, for example, only before doing a push.
