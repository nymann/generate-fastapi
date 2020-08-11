import pytest
from fastapi_code_generator.parsers import json_parser


def test_parser():
    columns = json_parser.parse_json('example.json')
    assert len(columns) == 1
