"""Example Google style docstrings.

"""
import pathlib
import subprocess
import sys

import pytest
from fastapi import testclient

import ${PROJECT_NAME}


@pytest.fixture
def app():
    """app.
    """
    return ${PROJECT_NAME}.create_app()


@pytest.fixture
def client(app):
    """client.

    Args:
        app:
    """
    cwd = pathlib.Path(__file__).parent.parent
    try:
        subprocess.check_call(["alembic", "upgrade", "head"], cwd=cwd)
    except subprocess.CalledProcessError:
        sys.exit(1)
    with testclient.TestClient(app, "http://localhost:9001") as test_client:
        yield test_client
