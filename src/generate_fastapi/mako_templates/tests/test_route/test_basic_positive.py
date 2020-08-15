"""Basic positive tests (happy paths).
This module executes API calls with valid required parameters.
Validation checks:
    Validate status code: All requests should return 2XX HTTP status codes.
    Validate payload: Response is a well-formed JSON object.
    Validate state: GET requests should not change state.
    Validate headers: Verifies if headers are the same as expected.
"""

import datetime

import pydantic
import pytest
from requests import exceptions

from tests import test_${model.names.plural_name}, utils


def test_validate_status_codes(client):

    ${model.names.singular_name} = test_${model.names.plural_name}.mock_${model.names.singular_name}()

    # Get ${model.names.singular_name} list should give 200 OK
    data, status_code = test_${model.names.plural_name}.get_${model.names.plural_name}(client=client, from_date=datetime.datetime.min,to_date=datetime.datetime.max)
    assert status_code == 200

    # For create methods we expect 201 Created
    data, status_code = test_${model.names.plural_name}.create_${model.names.singular_name}(client=client,
                                                       ${model.names.singular_name}=${model.names.singular_name})
    assert status_code == 200
    ${PRIMARY_KEY_NAME} = data["${PRIMARY_KEY_NAME}"]

    # Retrieve, we expect 200 OK here.
    data, status_code = test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    assert status_code == 200

    # Delete, since we are returning the deleted ${model.names.singular_name}, a 200 OK is expected
    # instead of 204 No Content.
    data, status_code = test_${model.names.plural_name}.delete_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    assert status_code == 200


def test_validate_payload(client):
    ${model.names.singular_name} = test_${model.names.plural_name}.mock_${model.names.singular_name}()

    # Check if the payload when creating a ${model.names.singular_name} matches what we thing.
    data, _ = test_${model.names.plural_name}.create_${model.names.singular_name}(client=client, ${model.names.singular_name}=${model.names.singular_name})

    # API should save the email as lowercase.
    test_${model.names.plural_name}.no_state_change(data=data, ${model.names.singular_name}=${model.names.singular_name})

    # Check if the provided ${PRIMARY_KEY_NAME} (UUID4) is valid
    ${PRIMARY_KEY_NAME} = data["${PRIMARY_KEY_NAME}"]
    # Check if valid ${PRIMARY_KEY_NAME} TODO

    data, _ = test_${model.names.plural_name}.get_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    test_${model.names.plural_name}.no_state_change(data=data, ${model.names.singular_name}=${model.names.singular_name})

    # Delete, since we are returning the deleted ${model.names.singular_name}, a 200 OK is expected
    data, status_code = test_${model.names.plural_name}.delete_${model.names.singular_name}(client=client, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    test_${model.names.plural_name}.no_state_change(data=data, ${model.names.singular_name}=${model.names.singular_name})


def test_validate_headers(client):
    pass


def test_performance_sanity(client):
    mock_${model.names.singular_name} = test_${model.names.plural_name}.mock_${model.names.singular_name}()

    @utils.time_it
    def create(c, u):
        return test_${model.names.plural_name}.create_${model.names.singular_name}(client=c, ${model.names.singular_name}=u)

    ${model.names.singular_name}, _ = create(c=client, u=mock_${model.names.singular_name})

    @utils.time_it
    def get(c, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}):
        return test_${model.names.plural_name}.get_${model.names.singular_name}(client=c, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

    get(c=client, ${PRIMARY_KEY_NAME}=${model.names.singular_name}["${PRIMARY_KEY_NAME}"])

    @utils.time_it
    def delete(c, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}):
        return test_${model.names.plural_name}.delete_${model.names.singular_name}(client=c, ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

    delete(c=client, ${PRIMARY_KEY_NAME}=${model.names.singular_name}["${PRIMARY_KEY_NAME}"])
