"""Basic positive tests (happy paths).
This module executes API calls with valid required parameters.
Validation checks:
    Validate status code: All requests should return 2XX HTTP status codes.
    Validate payload: Response is a well-formed JSON object.
    Validate state: GET requests should not change state.
    Validate headers: Verifies if headers are the same as expected.
"""

import datetime
import uuid
from os import stat_result

import pydantic
import pytest
import requests
from requests import exceptions

from tests import test_${model.names.plural_name}, utils
from tests.test_${model.names.plural_name} import mock_${model.names.singular_name}

<%! from generate_fastapi.translators.json_translator import JsonTranslator %>


def test_validate_status_codes(client):
    ${PRIMARY_KEY_NAME} = str(${JsonTranslator.translate_pytype_to_rand_data(PRIMARY_KEY_TYPE)})
    bad_${model.names.singular_name} = test_${model.names.plural_name}.invalid_${model.names.singular_name}()

    try:
        _, _ = test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    except exceptions.HTTPError as e:
        assert e.response.status_code == 404

    try:
        _, status_code = test_${model.names.plural_name}.create_${model.names.singular_name}(client=client,
                                                ${model.names.singular_name}=bad_${model.names.singular_name})
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert e.response.status_code == 422

    ${model.names.singular_name} = test_${model.names.plural_name}.mock_${model.names.singular_name}()

    data, _ = test_${model.names.plural_name}.create_${model.names.singular_name}(client=client,${model.names.singular_name}=${model.names.singular_name})

    try:
        _, status_code = test_${model.names.plural_name}.update_${model.names.singular_name}(client=client, ${model.names.singular_name}=bad_${model.names.singular_name}, ${PRIMARY_KEY_NAME}=data["${PRIMARY_KEY_NAME}"])
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert e.response.status_code == 405

def test_validate_payload(client):
    ${PRIMARY_KEY_NAME} = str(${JsonTranslator.translate_pytype_to_rand_data(PRIMARY_KEY_TYPE)})
    try:
        _, status_code = test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert eval(e.response.text)["detail"] == "Log entry with id: '{0}' not found.".format(${PRIMARY_KEY_NAME})

    bad_${model.names.singular_name} = test_${model.names.plural_name}.invalid_${model.names.singular_name}()

    try:
        _, status_code = test_${model.names.plural_name}.create_${model.names.singular_name}(client=client,
                                                ${model.names.singular_name}=bad_${model.names.singular_name})
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert eval(e.response.text)["detail"][0]["msg"] == "invalid date format"

    ${model.names.singular_name} = test_${model.names.plural_name}.mock_${model.names.singular_name}()

    data, _ = test_${model.names.plural_name}.create_${model.names.singular_name}(client=client,${model.names.singular_name}=${model.names.singular_name})

    try:
        _, status_code = test_${model.names.plural_name}.update_${model.names.singular_name}(client=client, ${model.names.singular_name}=bad_${model.names.singular_name}, ${PRIMARY_KEY_NAME}=data["${PRIMARY_KEY_NAME}"])
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert eval(e.response.text)["detail"] == "Method Not Allowed"

def test_validate_headers(client):
    pass

def test_performance_sanity(client):
    ${model.names.singular_name} = test_${model.names.plural_name}.mock_${model.names.singular_name}()
    bad_${model.names.singular_name} = test_${model.names.plural_name}.invalid_${model.names.singular_name}()
    ${PRIMARY_KEY_NAME} = str(${JsonTranslator.translate_pytype_to_rand_data(PRIMARY_KEY_TYPE)})

    @utils.time_it
    def get(client, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}):
        return test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

    try:
        _, status_code = get(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200
    except exceptions.HTTPError as _:
        pass

    @utils.time_it
    def update(client, ${model.names.singular_name}, ${PRIMARY_KEY_NAME}):
        return test_${model.names.plural_name}.update_${model.names.singular_name}(client=client, ${model.names.singular_name}=${model.names.singular_name}, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

    data, _ = test_${model.names.plural_name}.create_${model.names.singular_name}(client=client,${model.names.singular_name}=${model.names.singular_name})

    try:
        _, status_code = update(client=client, ${model.names.singular_name}=bad_${model.names.singular_name}, ${PRIMARY_KEY_NAME}=data["${PRIMARY_KEY_NAME}"])
        assert status_code != 200
    except exceptions.HTTPError as _:
        pass

    @utils.time_it
    def create(client, ${model.names.singular_name}):
        return test_${model.names.plural_name}.create_${model.names.singular_name}(client=client, ${model.names.singular_name}=${model.names.singular_name})

    try:
        _, status_code = create(client=client,${model.names.singular_name}=bad_${model.names.singular_name})
        assert status_code != 200
    except exceptions.HTTPError as _:
        pass
