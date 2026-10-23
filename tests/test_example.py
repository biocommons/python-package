from biocommons.template_py import __version__, get_quote_from_marvin


def test_version():
    """package exposes __version__ (resolved from installed metadata)"""
    assert __version__ is not None


def test_get_quote_from_marvin():
    """get_quote_from_marvin is re-exported at package top level and returns a quote"""
    assert get_quote_from_marvin() is not None
