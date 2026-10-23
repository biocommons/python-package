from biocommons.template_py.marvin import get_quote


def test_get_quote():
    assert get_quote() is not None
