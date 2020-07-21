"""This module is for schemas related to PLURAL.

These schemas are used for creating new instances of SINGULAR. Returning paginated
result (`Paginated`) and transforming a SINGULAR

"""
import datetime
from typing import List
from xml.etree import ElementTree as ET

import pydantic

from PROJECT_NAME.domain import base_schemas


class _Base(pydantic.BaseModel):
    """Used as baseclass for all other schemas inside this module.

    The base schema is kept private (by leftpadding with `_`).
    """


BASE_FIELDS


class Create(_Base):
    """Create schema is used for validating POST requests.
    """


class DB(_Base):
    """DB schema is used for transforming an ORM model to a pydantic model.
    """

    PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE

    class Config:
        """We set orm_mode to True to allow transforming the ORM model.
        """

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
