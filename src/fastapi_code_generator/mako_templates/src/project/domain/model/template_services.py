"""This module is for implementing ${model.names.singular_name} services.

The Service class' job is to interface with the ${model.names.singular_name} queries, and
transform the result provided by the Quries class into Schemas. When
creating an instance of Service() you shouldn't call
`service._queries()` directly, hence why it's declared as private (_).
"""

from typing import List, Optional

import pydantic

from ${PROJECT_NAME}.domain import base_schemas
from ${PROJECT_NAME}.domain.${model.names.plural_name} import (
    ${model.names.singular_name}_queries, ${model.names.singular_name}_schemas)


class Service:
    """Service."""

    def __init__(self, queries: ${model.names.singular_name}_queries.Queries):
        """__init__.

        Args:
            queries (${model.names.singular_name}_queries.Queries): queries
        """
        self._queries = queries

    async def create(self,
                     ${model.names.singular_name}: ${model.names.singular_name}_schemas.Create) -> ${model.names.singular_name}_schemas.DB:
        """create.

        Args:
            ${model.names.singular_name} (${model.names.singular_name}_schemas.Create): ${model.names.singular_name}
        Returns:
            ${model.names.singular_name}_schemas.DB:
        """
        new_${model.names.singular_name} = await self._queries.create(${model.names.singular_name}=${model.names.singular_name})
        return ${model.names.singular_name}_schemas.DB.from_orm(new_${model.names.singular_name})

    async def get_by_id(
            self, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}) -> ${model.names.singular_name}_schemas.DB:
        """Gets the ${model.names.singular_name} that matches the provided ${PRIMARY_KEY_NAME}.

        Args:
            ${PRIMARY_KEY_NAME} (${PRIMARY_KEY_TYPE}): ${PRIMARY_KEY_NAME}
        Returns:
            ${model.names.singular_name}_schemas.DB: If the ${model.names.singular_name} is found, otherwise 404.
        """
        ${model.names.singular_name} = await self._queries.get_by_id(
            ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        if ${model.names.singular_name}:
            return ${model.names.singular_name}_schemas.DB.from_orm(${model.names.singular_name})
        return None

    async def get_list(
        self,
        page: pydantic.conint(ge=1),
        page_size: pydantic.conint(ge=1, le=100),
    ) -> ${model.names.singular_name}_schemas.Paginated:
        """Gets a paginated result list of ${model.names.plural_name}.

        Args:
            page (pydantic.conint(ge=1)): page
            page_size (pydantic.conint(ge=1, le=100)): page_size
        Returns:
            ${model.names.singular_name}_schemas.Paginated:
        """
        ${model.names.plural_name}, total = await self._queries.get_list(page=page,
                                                     page_size=page_size)
        more = ((total / page_size) - page) > 0
        results = [
            ${model.names.singular_name}_schemas.DB.from_orm(${model.names.singular_name}) for ${model.names.singular_name} in ${model.names.plural_name}
        ]
        pagination = base_schemas.Pagination(total=total, more=more)
        return ${model.names.singular_name}_schemas.Paginated(results=results,
                                          pagination=pagination)

    async def update(
            self, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE},
            new_${model.names.singular_name}: ${model.names.singular_name}_schemas.Update) -> ${model.names.singular_name}_schemas.DB:
        """Updates an existing ${model.names.singular_name}.

        Args:
            ${PRIMARY_KEY_NAME} (${PRIMARY_KEY_TYPE}): ${PRIMARY_KEY_NAME}
            new_${model.names.singular_name} (${model.names.singular_name}_schemas.Update): new_${model.names.singular_name}
        Returns:
            ${model.names.singular_name}_schemas.DB:
        """
        old_${model.names.singular_name} = await self._queries.get_by_id(
            ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})

        updated_${model.names.singular_name} = await self._queries.update(old_${model.names.singular_name}=old_${model.names.singular_name},
                                                      new_${model.names.singular_name}=new_${model.names.singular_name})
        return ${model.names.singular_name}_schemas.DB.from_orm(updated_${model.names.singular_name})

    async def delete(self,
                     ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}) -> ${model.names.singular_name}_schemas.DB:
        """Deletes a specific ${model.names.singular_name}
        Args:
            ${PRIMARY_KEY_NAME} (${PRIMARY_KEY_TYPE}): ${PRIMARY_KEY_NAME}
        Returns:
            ${model.names.singular_name}_schemas.DB:
        """
        deleted_${model.names.singular_name} = await self._queries.delete(
            ${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
        return ${model.names.singular_name}_schemas.DB.from_orm(deleted_${model.names.singular_name})
