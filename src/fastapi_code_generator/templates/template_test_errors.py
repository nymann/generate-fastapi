"""General test of CRUD
"""
from tests import test_PLURAL


def test_retrieve_on_non_existing_SINGULAR_returns_404(client):
