"""biocommons.python_package package"""

from importlib.metadata import PackageNotFoundError, version

from .marvin import get_quote as get_quote_from_marvin  # noqa: F401

try:
    __version__ = version(__package__)
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    __version__ = None
