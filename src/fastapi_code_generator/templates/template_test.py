"""Test CRUD operations."""
import datetime
import random
import string
import uuid

import pydantic
from requests import exceptions

import pytest

BASE_ROUTE = '/PLURAL/'


def create_SINGULAR(client COMMA_SEPARATED_FIELDS):
    """create_SINGULAR.

        Args:
    BASE_FIELDS
    """
    SINGULAR = dict(COMMA_SEPARATED_COLNAMES)
    response = client.post(BASE_ROUTE, json=SINGULAR)
    response.raise_for_status()
    return response.json()


def retrieve_SINGULAR(client,
                      PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE,
                      expected_found: bool = True):
    """retrieve_SINGULAR.

    Args:
        client:
        PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
        expected_found (bool): expected_found
    """
    response = client.get(f'{BASE_ROUTE}{PRIMARY_KEY_NAME}')
    response.raise_for_status()
    if expected_found:
        assert response.status_code == 200
    else:
        assert response.status_code == 404
    return response.json()


def delete_SINGULAR(client, PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE):
    """delete_SINGULAR.

    Args:
        client:
        PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
    """
    route = f'{BASE_ROUTE}{PRIMARY_KEY_NAME}'
    response = client.delete(route)
    response.raise_for_status()
    data = response.json()
    assert data['PRIMARY_KEY_NAME'] == PRIMARY_KEY_NAME
    assert client.get(route).status_code == 404


def get_all_PLURAL(client):
    """get_all_PLURAL.

    Args:
        client:
    """
    response = client.get(BASE_ROUTE)
    response.raise_for_status()


def rand_bool():
    return bool(random.randint(0, 1))


def rand_date():
    return datetime.date.today() + datetime.timedelta(random.randint(1, 365))


def rand_datetime():
    return datetime.datetime.now() + datetime.timedelta(
        days=random.randint(1, 365),
        hours=random.randint(1, 23),
        minutes=random.randint(1, 59),
        seconds=random.randint(1, 60),
        microseconds=random.randint(1, 100))


def rand(length: int) -> str:
    """rand.

    Args:
        length (int): length
    Returns:
        str:
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
