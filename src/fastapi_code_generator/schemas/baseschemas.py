"""Baseschemas.

Returns:
    [type]: [description]
"""

from dataclasses import dataclass
from typing import List, Optional

import pydantic


class FieldType(pydantic.BaseModel):
    """FieldType."""

    name: str
    max_length: Optional[pydantic.conint(ge=1)]
    min_length: Optional[pydantic.conint(ge=1)]
    nullable: bool = True
    default: Optional[str] = None


class Field(pydantic.BaseModel):
    """Field."""

    name: str
    field_type: FieldType
    is_primary_key: bool


class Route(pydantic.BaseModel):
    """Route."""

    name: str
    include: bool


class Names(pydantic.BaseModel):
    """Names."""

    singular_name: str
    plural_name: str


@dataclass
class Model:
    """Model."""

    fields: List[Field]
    routes: List[Route]
    names: Names
