"""[summary].

Returns:
    [type]: [description]
"""

import json

import inflect

from generate_fastapi.schemas import baseschemas


def parse_json(path):
    """parse_json.

    Args:
        path ([type]): [description]

    Returns:
        [type]: [description]
    """
    with open(path) as json_file:
        file_content = json.load(json_file)

        models = []
        for key in file_content.get('models').keys():
            json_model = file_content.get('models').get(key)

            fields = _parse_fields(json_model)
            models.append(
                baseschemas.Model(
                    fields=fields,
                    routes=_parse_routes(json_model),
                    names=_parse_names(key),
                ), )

        return models


def _parse_field_type(field):
    default = None
    if 'default' in field:
        default = field.get('default')

    nullable = False
    if 'required' in field:
        nullable = not field.get('required')

    field_type = field.get('type')
    min_length = None
    if 'min_length' in field_type:
        min_length = field.get('type').get('min_length')

    max_length = None
    if 'max_length' in field_type:
        max_length = field_type.get('max_length')

    return baseschemas.FieldType(
        name=field_type.get('name'),
        max_length=max_length,
        min_length=min_length,
        nullable=nullable,
        default=default,
    )


def _parse_fields(json_model):
    fields = []
    for field in json_model.get('fields'):
        field_type = _parse_field_type(field)

        is_primary_key = False
        if 'is_primary_key' in field:
            is_primary_key = field.get('is_primary_key')

        fields.append(
            baseschemas.Field(
                name=field.get('name'),
                field_type=field_type,
                is_primary_key=is_primary_key,
            ), )
    return fields


def _parse_routes(json_model):
    routes = []
    for route in json_model.get('routes'):
        routes.append(
            baseschemas.Route(
                name=route.get('name'),
                include=route.get('include'),
            ), )
    return routes


def _parse_names(singular_name):
    engine = inflect.engine()
    plural_name = engine.plural_noun(singular_name)
    return baseschemas.Names(
        singular_name=singular_name,
        plural_name=plural_name,
    )
