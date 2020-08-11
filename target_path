"""This module is for implementing SINGULAR services.

The Service class' job is to interface with the SINGULAR queries, and
transform the result provided by the Quries class into Schemas. When
creating an instance of Service() you shouldn't call
`service._queries()` directly, hence why it's declared as private (_).
"""

from typing import List, Optional

import pydantic

from PROJECT_NAME.domain import base_schemas
from PROJECT_NAME.domain.PLURAL import SINGULAR_queries, SINGULAR_schemas


class Service:
    """Service."""

    def __init__(self, queries: SINGULAR_queries.Queries):
        """__init__.

        Args:
            queries (SINGULAR_queries.Queries): queries
        """
        self._queries = queries

    async def create(self,
                     SINGULAR: SINGULAR_schemas.Create) -> SINGULAR_schemas.DB:
        """create.

        Args:
            SINGULAR (SINGULAR_schemas.Create): SINGULAR
        Returns:
            SINGULAR_schemas.DB:
        """
        new_SINGULAR = await self._queries.create(SINGULAR=SINGULAR)
        return SINGULAR_schemas.DB.from_orm(new_SINGULAR)

    async def get_by_id(
            self, PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE) -> SINGULAR_schemas.DB:
        """Gets the SINGULAR that matches the provided PRIMARY_KEY_NAME.

        Args:
            PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
        Returns:
            SINGULAR_schemas.DB: If the SINGULAR is found, otherwise 404.
        """
        SINGULAR = await self._queries.get_by_id(
            PRIMARY_KEY_NAME=PRIMARY_KEY_NAME)
        if SINGULAR:
            return SINGULAR_schemas.DB.from_orm(SINGULAR)
        return None

    async def get_list(
        self,
        page: pydantic.conint(ge=1),
        page_size: pydantic.conint(ge=1, le=100),
    ) -> SINGULAR_schemas.Paginated:
        """Gets a paginated result list of PLURAL.

        Args:
            page (pydantic.conint(ge=1)): page
            page_size (pydantic.conint(ge=1, le=100)): page_size
        Returns:
            SINGULAR_schemas.Paginated:
        """
        PLURAL, total = await self._queries.get_list(page=page,
                                                     page_size=page_size)
        more = ((total / page_size) - page) > 0
        results = [
            SINGULAR_schemas.DB.from_orm(SINGULAR) for SINGULAR in PLURAL
        ]
        pagination = base_schemas.Pagination(total=total, more=more)
        return SINGULAR_schemas.Paginated(results=results,
                                          pagination=pagination)

    async def update(
            self, PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE,
            new_SINGULAR: SINGULAR_schemas.Update) -> SINGULAR_schemas.DB:
        """Updates an existing SINGULAR.

        Args:
            PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
            new_SINGULAR (SINGULAR_schemas.Update): new_SINGULAR
        Returns:
            SINGULAR_schemas.DB:
        """
        old_SINGULAR = await self._queries.get_by_id(
            PRIMARY_KEY_NAME=PRIMARY_KEY_NAME)

        updated_SINGULAR = await self._queries.update(old_SINGULAR=old_SINGULAR,
                                                      new_SINGULAR=new_SINGULAR)
        return SINGULAR_schemas.DB.from_orm(updated_SINGULAR)

    async def delete(self,
                     PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE) -> SINGULAR_schemas.DB:
        """Deletes a specific SINGULAR
        Args:
            PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
        Returns:
            SINGULAR_schemas.DB:
        """
        deleted_SINGULAR = await self._queries.delete(
            PRIMARY_KEY_NAME=PRIMARY_KEY_NAME)
        return SINGULAR_schemas.DB.from_orm(deleted_SINGULAR)
