# biocommons.template_py

[![Release](https://img.shields.io/github/v/release/biocommons/template-py)](https://img.shields.io/github/v/release/biocommons/template-py)
[![Build status](https://img.shields.io/github/actions/workflow/status/biocommons/template-py/main.yml?branch=main)](https://github.com/biocommons/template-py/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/biocommons/template-py/branch/main/graph/badge.svg)](https://codecov.io/gh/biocommons/template-py)
[![Commit activity](https://img.shields.io/github/commit-activity/m/biocommons/template-py)](https://img.shields.io/github/commit-activity/m/biocommons/template-py)
[![License](https://img.shields.io/github/license/biocommons/template-py)](https://img.shields.io/github/license/biocommons/template-py)

## Package Description

This project is a product of the [biocommons](https://biocommons.org/) community.

- **Github repository**: <https://github.com/biocommons/template-py/>
- **Documentation** <https://biocommons.github.io/template-py/>

## Getting Help

- 🐛 **Bug reports**: [Open an issue](../../issues/new?template=bug_report.md)
- 💡 **Feature requests**: [Open an issue](../../issues/new?template=feature_request.md)
- ❓ **Questions**: [Ask in biocommons/discussions](https://github.com/biocommons/discussions)
- 💬 **General discussion**: [biocommons/discussions](https://github.com/biocommons/discussions)

## Python Package Installation

Install from PyPI with `pip install biocommons.template_py` or `uv pip install biocommons.template_py`, then try it:

    $ source venv/bin/activate

    $ python3 -m biocommons.template_py
    Marvin says:
    There's only one life-form as intelligent as me within thirty parsecs...

    $ marvin-quote
    Marvin says:
    You think you've got problems? What are you supposed to do if you...

    $ ipython
    >>> from biocommons.template_py import __version__, get_quote_from_marvin
    >>> __version__
    '0.1.dev8+gd5519a8.d20211123'
    >>> get_quote()
    "The first ten million years were the worst, ...


## Developer Setup

### Install Prerequisites

These tools are required to get started:

- [git](https://git-scm.com/): Version control system
- [GNU make](https://www.gnu.org/software/make/): Current mechanism for consistent invocation of developer tools.
- [uv](https://docs.astral.sh/uv/): An extremely fast Python package and project manager, written in Rust.

#### MacOS or Linux Systems

- [Install brew](https://brew.sh/)
- `brew install git make uv`

#### Linux (Debian-based systems)

You may also install using distribution packages:

    sudo apt install git make

Then install uv using the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

### One-time developer setup

Create a Python virtual environment, install dependencies, install git hooks (prek), and install an editable package:

    make devready

### Development

**N.B.** Developers are strongly encouraged to use `make` to invoke tools to
ensure consistency with the CI/CD pipelines.  Type `make` to see a list of
supported targets.  A subset are listed here:

    » make
    🌟🌟 biocommons conventional make targets 🌟🌟

    Using these targets promots consistency between local development and ci/cd commands.

    usage: make [target ...]

    BASIC USAGE
    help                Display help message

    SETUP, INSTALLATION, PACKAGING
    devready            Prepare local dev env: Create virtual env, install the git hooks (prek)
    build               Build package
    publish             publish package to PyPI

    FORMATTING, TESTING, AND CODE QUALITY
    cqa                 Run code quality assessments
    test                Test the code with pytest
    test-coverage       Test the code with pytest and generate coverage report
    test-matrix         Test with each supported Python version (via nox)

    DOCUMENTATION
    docs-serve          Build and serve the documentation
    docs-test           Test if documentation can be built without warnings or errors
    docs-deploy         Deploy documentation to GitHub Pages

    CLEANUP
    clean               Remove temporary and backup files
    cleaner             Remove files and directories that are easily rebuilt
    cleanest            Remove all files that can be rebuilt
    distclean           Remove untracked files and other detritus

### Testing

    make test            # tests, no coverage
    make test-coverage   # tests with coverage; writes coverage.xml
    make test-matrix     # `make test` on each Python version listed in pyproject.toml classifiers (nox)

`make test` is the test command everywhere: locally, in each nox session, and in each CI matrix leg. One CI leg runs `make test-coverage` and uploads to Codecov instead.

Known limitation: nox does not forward arguments, so `nox -- -k foo` runs the full suite. Run one version with `uv run nox -s tests-3.11`, or a subset on one version with `uv run --isolated --python 3.11 pytest -k foo` (`--isolated` leaves `.venv` untouched).

#### VS Code

Testing → Configure Python Tests → pytest → root directory. No other settings are needed; coverage is off by default, so breakpoints work.

#### Coverage gate

Codecov's `codecov/project` status fails when coverage drops more than 0.5% from the base commit. Make `codecov/project` a required status check in branch protection, or the gate does nothing.
