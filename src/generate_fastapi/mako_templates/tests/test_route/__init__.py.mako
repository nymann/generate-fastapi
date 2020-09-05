import random
from typing import Any, Dict, Tuple

import pydantic
import pytest
from requests import exceptions

from tests import utils

<%! from generate_fastapi.translators.json_translator import JsonTranslator %>


ROUTE = "/${model.names.plural_name}/"


def raise_for_status(func):

    def wrapper(*args, **kwargs) -> Tuple[Dict[str, Any], int]:
        print(f"Called wrapper with function: '{func.__name__}'.")
        print(f"args: '{args}', kwargs '{kwargs}'.")
        response = func(*args, **kwargs)
        print(f"response saved, status code: {response.status_code}")
        response.raise_for_status()
        return response.json(), response.status_code

    return wrapper


@raise_for_status
def create_${model.names.singular_name}(client, ${model.names.singular_name}: dict):
    return client.post(ROUTE, json=${model.names.singular_name})


@raise_for_status
def update_${model.names.singular_name}(client, ${model.names.singular_name}: dict, ${PRIMARY_KEY_NAME}: str):
    return client.put(ROUTE + ${PRIMARY_KEY_NAME}, json=${model.names.singular_name})


@raise_for_status
def delete_${model.names.singular_name}(client, ${PRIMARY_KEY_NAME}: str):
    return client.delete(ROUTE + ${PRIMARY_KEY_NAME})


@raise_for_status
def get_${model.names.singular_name}(client, ${PRIMARY_KEY_NAME}: str):
    return client.get(ROUTE + ${PRIMARY_KEY_NAME})


@raise_for_status
def get_${model.names.plural_name}(client, page: int = 1, page_size: int = 50):
    return client.get(ROUTE, params={
                        'page': page,
                        'page_size':page_size
                        })


def mock_${model.names.singular_name}():
    return {
        % for field in model.fields:
        % if not field.is_primary_key:
        "${field.name}": ${JsonTranslator.translate_typename_to_rand_data(field.field_type.name)},
        % endif
        % endfor
    }

def invalid_${model.names.singular_name}():
    return {
        % for field in model.fields:
        % if not field.is_primary_key:
        "${field.name}": ${JsonTranslator.translate_typename_to_invalid_data(field.field_type.name)},
        % endif
        % endfor
    }

def no_state_change(data: Dict[str, Any],
                    ${model.names.singular_name}: Dict[str, Any]) -> None:
    for key, value in data.items():
        if key != "${PRIMARY_KEY_NAME}":
            assert ${model.names.singular_name}[key] == value
