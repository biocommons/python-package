from biocommons.template_py.marvin import get_quote


def test_get_quote():
    """marvin.get_quote returns a quote (tests/ twin of src-adjacent marvin_adjacent_test.py)"""
    assert get_quote() is not None
