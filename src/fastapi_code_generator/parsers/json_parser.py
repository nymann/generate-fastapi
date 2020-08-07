import json
from dataclasses import fields

import inflect

from fastapi_code_generator.schemas import baseschemas


def parse_json(path):
    with open(path) as file:
        data = json.load(file)

        models = []
        for key in data['models'].keys():
            json_model = data['models'][key]
            fields = _parse_fields(json_model)
            names = _parse_names(key)
            routes = _parse_routes(json_model)

            models.append(
                baseschemas.Model(fields=fields, routes=routes, names=names))

        return models


def _parse_fields(json_model):
    fields = []
    for field in json_model['fields']:
        field_name = field['name']
        field_type_name = field['type']['name']

        default = None
        if 'default' in field:
            default = field['default']

        nullable = False
        if 'required' in field:
            nullable = not field['required']

        min_length = None
        if 'min_length' in field['type']:
            min_length = field['type']['min_length']

        max_length = None
        if 'max_length' in field['type']:
            max_length = field['type']['max_length']

        field_type = baseschemas.FieldType(name=field_type_name,
                                           max_length=max_length,
                                           min_length=min_length,
                                           nullable=nullable,
                                           default=default)

        is_primary_key = False
        if 'is_primary_key' in field:
            is_primary_key = field['is_primary_key']

        fields.append(
            baseschemas.Field(name=field_name,
                              type=field_type,
                              is_primary_key=is_primary_key))
    return fields


def _parse_routes(json_model):
    routes = []
    for route in json_model['routes']:
        routes.append(
            baseschemas.Route(name=route['name'], include=route['include']))
    return routes


def _parse_names(singular_name):
    engine = inflect.engine()
    plural_name = engine.plural_noun(singular_name)
    return baseschemas.Names(singular_name=singular_name,
                             plural_name=plural_name)
