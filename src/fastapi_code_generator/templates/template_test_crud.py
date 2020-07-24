"""General test of CRUD
"""
from tests import test_PLURAL


def test_crud(client):
    """test_crud.

    Args:
        client:
    """
    request = {RANDOM_MOCKDATA}
    # create
    data = test_PLURAL.create_SINGULAR(client, **request)
    PRIMARY_KEY_NAME = data["PRIMARY_KEY_NAME"]

    # retrieve
    test_PLURAL.retrieve_SINGULAR(client=client,
                                  PRIMARY_KEY_NAME=PRIMARY_KEY_NAME)

    # delete
    test_PLURAL.delete_SINGULAR(client=client,
                                PRIMARY_KEY_NAME=PRIMARY_KEY_NAME)

    # retrieve all with nothing returns nothing
    test_PLURAL.get_all_PLURAL(client=client)
