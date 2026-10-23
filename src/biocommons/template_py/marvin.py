"""random quotes from Marvin the depressed robot

The secret is to bang the rocks together.

"""

import importlib.resources
import logging
import random

import yaml

_logger = logging.getLogger(__name__)


quotes_stream = importlib.resources.files(__package__).joinpath("_data/quotes.yaml").read_text()
quotes = yaml.load(quotes_stream, Loader=yaml.SafeLoader)["quotes"]


def is_alive() -> bool:
    """tests whether Marvin is alive

    >>> is_alive() is True
    True

    """
    return True


def get_quote() -> str:
    """return random Marvin quote

    eg> get_quote()
    "There's only one life-form as intelligent..."

    """
    _logger.info("Getting quote from Marvin")

    quote = random.choice(quotes)  # noqa: S311

    _logger.info("Got quote from Marvin (len=%s)", len(quote))

    return quote
