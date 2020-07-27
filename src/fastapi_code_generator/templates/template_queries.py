import datetime
from typing import List
from typing import Tuple

import pydantic

from PROJECT_NAME.core.db import DB
from PROJECT_NAME.domain.PLURAL import SINGULAR_model
from PROJECT_NAME.domain.PLURAL import SINGULAR_schemas

CreateSchema = SINGULAR_schemas.Create
UpdateSchema = SINGULAR_schemas.Update
Model = SINGULAR_model.Model


class Queries():

    async def create(self, SINGULAR: CreateSchema) -> Model:
        return await Model.create(**SINGULAR.__dict__)

    async def get_list(self, page_size: int,
                       page: int) -> Tuple[List[Model], int]:
        PLURAL: List[Model] = await Model.query.order_by(
            Model.PRIMARY_KEY_NAME.asc()).offset(page_size * (page - 1)
                                                 ).limit(page_size).gino.all()

        count = await DB.func.count(Model.PRIMARY_KEY_NAME).gino.scalar()
        return PLURAL, count

    async def get_by_id(self, PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE) -> Model:
        return await Model.get(PRIMARY_KEY_NAME)

    async def delete(self, PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE) -> Model:
        SINGULAR = await self.get_by_id(PRIMARY_KEY_NAME)
        await SINGULAR.delete()
        return SINGULAR

    async def update(self, old_SINGULAR: Model,
                     new_SINGULAR: UpdateSchema) -> Model:
        updated_SINGULAR = await old_SINGULAR.update(**new_SINGULAR.__dict__
                                                     ).apply()
        return updated_SINGULAR._instance
