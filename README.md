[![CI wowkflow](https://github.com/hoppiece/python-dev-settings/actions/workflows/ci.yaml/badge.svg)](https://github.com/hoppiece/python-dev-settings/actions/workflows/ci.yaml)
## What's this
My settings when start a new Python project.


### 1. Tools setup
1. Set up python via pyenv
2. Setup poetry

Recomend set as 
```bash
pyenv install 3.x.x
pyenv shell 3.x.x 
poetry config --local virtualenvs.in-project true
poetry env use python
poetry install --no-root
```
Brief explanation.
- `pyenv install 3.x.x` -- Installing python to local. Search installable version by `pyenv install --list`. Your available version on the local can show by `pyenv versions`.
- `pyenv shell 3.x.x` --  Added the path to pyenv's 3.x.x on your current shell.
- `poetry config --local virtualenvs.in-project true` --  Poetry makes `.venv/` for virtual environment. If you want to set this as a global, need not. `--local` option (Setting as global is recommended if you use VSCode.)
- `poetry env use python` -- Poetry creates the vertualenv specified the python path. In this case, Poetry uses the pyenv's Python 3.x.x path, and creates the `.venv` directory.
- `poetry install --no-root` -- Poetry installs dependencies.
    - If you develop a python package (i.e., your project has a directory the same as a package name and the directory contains your package source code), need not `--no-root` option.

IDEs detect `.venv` directory and activate the virtualenv automatically on it's terminal. If you run in a primitive shell, activate the virtualenv by `source .venv/bin/activate`, or tell virtualenv to Poetry by `poetry run python <your script>`.


### 2. Install tools via Poetry
Install development support tools such as Linter.
```bash
poetry add black isort flake8 mypy pytest pytest-cov --group dev
```
Comment.
- The line length restriction is relaxed from pep8 to allow up to 99 characters.
- The `mypy` setup is based on this site: [Professional-grade mypy configuration](https://careers.wolt.com/en/blog/tech/professional-grade-mypy-configuration)


### 3. Configuate the tools

`pyproject.toml`
```toml
[tool.black]
line-length = 99
[tool.isort]
profile = "black"
line_length = 99
[tool.mypy]
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
```

`.flake8`
```toml
[flake8]
extend-ignore = E203
max-line-length = 99
```


`.github/workflows/ci.yaml`
```yaml
name: CI wowkflow

on:
  push:
  pull_request:
  schedule:
    # Monthly execution schedule for UTC.
    - cron: "3 3 5 * * "

jobs:
  CI:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os:
          - ubuntu-latest
        python-version: ["3.10", "3.11"]

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry config virtualenvs.create false
          poetry install --with dev --no-root # If your project is about python package, you need not `--no-root` option.
      - name: Lint and format check
        run: |
          black --check --diff .
          flake8 --show-source .
          isort --check-only --diff .
          mypy --show-column-numbers --show-error-context .
        continue-on-error: true
      - name: Test with pytest and doctest
        run: |
          pytest --cov --doctest-modules .
      - name: Upload coverge reports to Codecov via GitHub Actions
        uses: codecov/codecov-action@v3

```
