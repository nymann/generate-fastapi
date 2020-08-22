"""This module is for schemas related to ${model.names.plural_name}.

These schemas are used for creating new instances of ${model.names.singular_name}. Returning
paginated result (`Paginated`) and transforming a ${model.names.singular_name}

"""
import datetime
from dataclasses import field
from os import name
from typing import List
from xml.etree import ElementTree as ET

import pydantic

from ${PROJECT_NAME}.domain import base_schemas

<%! from generate_fastapi.translators.json_translator import JsonTranslator %>

class _Base(pydantic.BaseModel):
    """Used as baseclass for all other schemas inside this module.

    The base schema is kept private (by leftpadding with `_`).
    """

% for field in model.fields:
    % if not field.is_primary_key:
    % if field.field_type.nullable:
    ${field.name}: pydantic.Optional[${JsonTranslator.translate_typename_to_pytypes(field.field_type.name)}] = pydantic.Field(None${', max_length='+str(field.field_type.max_length) if field.field_type.max_length else ''}\
${', min_length='+str(field.field_type.min_length) if field.field_type.min_length else ''})
    % else:
    ${field.name}: ${JsonTranslator.translate_typename_to_pytypes(field.field_type.name)} = pydantic.Field(...${', max_length='+str(field.field_type.max_length) if field.field_type.max_length else ''}\
${', min_length='+str(field.field_type.min_length) if field.field_type.min_length else ''})
    %endif
    %endif
% endfor


class Create(_Base):
    """Create schema is used for validating POST requests."""

class Update(_Base):
    """Update schema is used for validating POST requests."""

class DB(_Base):
    """DB schema is used for transforming an ORM model to a pydantic model."""

    ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}

    class Config:
        """We set orm_mode to True to allow transforming the ORM model."""

        orm_mode = True


class Paginated(pydantic.BaseModel):
    """Paginated result schema.

    An example paginated result could look like this.
    return {
        results = [],
        pagination {
            more = True,
            total = 1000
        }
    }
    """

    results: List[DB]
    pagination: base_schemas.Pagination
