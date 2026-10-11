from biocommons.python_package import __version__, get_quote_from_marvin


def test_version():
    assert __version__ is not None


def test_get_quote_from_marvin():
    assert get_quote_from_marvin() is not None
