import datetime
from typing import List, Tuple

import pydantic

from ${PROJECT_NAME}.core.db import DB
from ${PROJECT_NAME}.domain.${model.names.plural_name} import (
    ${model.names.singular_name}_model, ${model.names.singular_name}_schemas)

CreateSchema = ${model.names.singular_name}_schemas.Create
UpdateSchema = ${model.names.singular_name}_schemas.Update
Model = ${model.names.singular_name}_model.Model


class Queries():

    async def create(self, ${model.names.singular_name}: CreateSchema) -> Model:
        return await Model.create(**${model.names.singular_name}.__dict__)

    async def get_list(self, page_size: int,
                       page: int) -> Tuple[List[Model], int]:
        ${model.names.plural_name}: List[Model] = await Model.query.order_by(
            Model.${PRIMARY_KEY_NAME}.asc()).offset(page_size * (page - 1)
                                                 ).limit(page_size).gino.all()

        count = await DB.func.count(Model.${PRIMARY_KEY_NAME}).gino.scalar()
        return ${model.names.plural_name}, count

    async def get_by_id(self, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}) -> Model:
        return await Model.get(${PRIMARY_KEY_NAME})

    async def delete(self, ${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE}) -> Model:
        ${model.names.singular_name} = await self.get_by_id(${PRIMARY_KEY_NAME})
        await ${model.names.singular_name}.delete()
        return ${model.names.singular_name}

    async def update(self, old_${model.names.singular_name}: Model,
                     new_${model.names.singular_name}: UpdateSchema) -> Model:
        updated_${model.names.singular_name} = await old_${model.names.singular_name}.update(**new_${model.names.singular_name}.__dict__
                                                     ).apply()
        return updated_${model.names.singular_name}._instance
