import pytest
from generate_fastapi.parsers import sql_parser

test_models = sql_parser.parse_sql('examples/example2.sql')


def test_one_model_is_parsed():
    assert len(test_models) == 1


def test_names_correctly_parsed():
    assert test_models[0].names.singular_name == 'user'
    assert test_models[0].names.plural_name == 'users'


def test_primary_key_correctly_parsed():
    assert any((field.name == 'identifier' and field.is_primary_key)
               for field in test_models[0].fields)


def test_check_nullable_false_per_default():
    assert any((field.name == 'is_admin' and field.field_type.nullable == True)
               for field in test_models[0].fields)
