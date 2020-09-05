import datetime
import random
import string
import time
import uuid
from dataclasses import field, fields

import pytest
from requests import exceptions

import mimesis

<%! from generate_fastapi.translators.json_translator import JsonTranslator %>


def random_string(length: int) -> str:
    """Get a random string of n length.
    Args:
        length (int): length
    Returns:
        str:
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def time_it(func):

    def wrapper(*args, **kwargs):
        started = time.time()
        result = func(*args, **kwargs)
        elapsed_seconds = time.time() - started
        elapsed_ms = round(elapsed_seconds * 1000)
        print(f"{func.__name__} took {elapsed_ms} ms to execute.")
        assert elapsed_ms < 200
        return result

    return wrapper


def random_datetime(start_year, end_year):
    generic_provider = mimesis.Generic()
    return generic_provider.datetime.datetime(start=start_year,
                                            end=end_year,
                                            timezone="Europe/Copenhagen")

def random_date(start_year, end_year):
    generic_provider = mimesis.Generic()
    return generic_provider.datetime.date(start=start_year,
                                            end=end_year)

def random_boolean():
    bool(random.getrandbits(1))
