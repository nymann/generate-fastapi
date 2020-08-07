""" Baseschemas.

Returns:
    [type]: [description]
"""

import dataclasses
from dataclasses import Field
from typing import Dict, List, Optional

import inflect
import pydantic

import sql_column_parser


class FieldType(pydantic.BaseModel):
    """ColumnType.
    """

    name: str
    max_length: Optional[pydantic.conint(ge=1)]
    min_length: Optional[pydantic.conint(ge=1)]
    nullable: bool = True
    default: Optional[str] = None


@dataclasses.dataclass
class Field:
    """Column.
    """

    name: str
    type: FieldType
    is_primary_key: bool


@dataclasses.dataclass
class Route:
    """Column.
    """

    name: str
    include: bool


@dataclasses.dataclass
class Names():
    """Names.
    """

    singular_name: str
    plural_name: str


@dataclasses.dataclass
class Model:
    """Table.
    """

    fields: List[Field]
    routes: List[Route]
    names: Names
