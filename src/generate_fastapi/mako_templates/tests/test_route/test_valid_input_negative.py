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

import pydantic
import pytest
import requests
from requests import exceptions

from tests import test_${model.names.plural_name}, utils
from tests.test_${model.names.plural_name} import mock_${model.names.singular_name}

<%! from generate_fastapi.translators.json_translator import JsonTranslator %>

def test_validate_status_codes(client):
    ${PRIMARY_KEY_NAME} = str(${JsonTranslator.translate_pytype_to_rand_data(PRIMARY_KEY_TYPE)})
    try:
        _, status_code = test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert e.response.status_code == 404

    try:
        ${model.names.singular_name} = mock_${model.names.singular_name}()
        _, status_code = test_${model.names.plural_name}.update_${model.names.singular_name}(client=client, ${model.names.singular_name}=${model.names.singular_name}, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert e.response.status_code == 405

    try:
        ${model.names.singular_name} = mock_${model.names.singular_name}()
        _, status_code = test_${model.names.plural_name}.delete_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert e.response.status_code == 404

def test_validate_payload(client):
    ${PRIMARY_KEY_NAME} = str(${JsonTranslator.translate_pytype_to_rand_data(PRIMARY_KEY_TYPE)})
    try:
        _, status_code = test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200
    except exceptions.HTTPError as e:
        assert eval(e.response.text)["detail"] == "${model.names.singular_name} with id: '{0}' not found.".format(${PRIMARY_KEY_NAME})

    try:
        ${model.names.singular_name} = mock_${model.names.singular_name}()
        _, status_code = test_${model.names.plural_name}.update_${model.names.singular_name}(client=client, ${model.names.singular_name}=${model.names.singular_name}, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200

    except exceptions.HTTPError as e:
        assert eval(e.response.text)["detail"] == "Method Not Allowed"

    try:
        ${model.names.singular_name} = mock_${model.names.singular_name}()
        _, status_code = test_${model.names.plural_name}.delete_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        assert status_code != 200

    except exceptions.HTTPError as e:
        assert eval(e.response.text)["detail"] == "${model.names.singular_name} with id: '{0}' not found.".format(${PRIMARY_KEY_NAME})

def test_validate_headers(client):
    pass


def test_performance_sanity(client):
    mock_${model.names.singular_name} = test_${model.names.plural_name}.mock_${model.names.singular_name}()
    ${PRIMARY_KEY_NAME} = str(${JsonTranslator.translate_pytype_to_rand_data(PRIMARY_KEY_TYPE)})

    @utils.time_it
    def update(client, ${model.names.singular_name}, ${PRIMARY_KEY_NAME}):
        return test_${model.names.plural_name}.update_${model.names.singular_name}(client=client, ${model.names.singular_name}=${model.names.singular_name}, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

    try:
        update(client=client, ${model.names.singular_name}=mock_${model.names.singular_name}, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    except exceptions.HTTPError:
        pass

    @utils.time_it
    def get(client, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}):
        return test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

    try:
        get(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    except exceptions.HTTPError:
        pass

    @utils.time_it
    def delete(client, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}):
        return test_${model.names.plural_name}.delete_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

    try:
        delete(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    except exceptions.HTTPError:
        pass
