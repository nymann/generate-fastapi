"""Endpoints starting with /PLURAL/ are defined here.

This module contains all API endpoints which path contains '/PLURAL/'.
Not that no "business-logic" is defined in here, we simply pass in onto
the SINGULAR service from the `service_factory`, by doing it this way
the controller only knows which methods it can call in SINGULAR Service
but nothing about the database.
"""

import fastapi
import pydantic
from starlette import status

from PROJECT_NAME.core import security, service_factory
from PROJECT_NAME.domain.PLURAL import SINGULAR_schemas

router = fastapi.APIRouter()


@router.get('/', response_model=SINGULAR_schemas.Paginated)
async def get_PLURAL(page_size: pydantic.conint(ge=1, le=100) = 20,
                     page: pydantic.conint(ge=1) = 1,
                     service=fastapi.Depends(
                         service_factory.get_SINGULAR_services)):
    """Get a paginated list of PLURAL.

    TODO(Add Doc)
    Args:
        page_size (pydantic.conint(ge=1, le=100)): page_size
        page (pydantic.conint(ge=1)): page
        service:
    """
    return await service.get_list(page=page, page_size=page_size)


@router.post('/',
             response_model=SINGULAR_schemas.DB,
             status_code=status.HTTP_201_CREATED)
async def add_SINGULAR(SINGULAR: SINGULAR_schemas.Create,
                       service=fastapi.Depends(
                           service_factory.get_SINGULAR_services)):
    """Create a new SINGULAR.

    TODO(Add Doc)
    Args:
        SINGULAR (SINGULAR_schemas.Create): SINGULAR
    """
    return await service.create(SINGULAR=SINGULAR)


@router.put('/{PRIMARY_KEY_NAME}', response_model=SINGULAR_schemas.DB)
async def update_SINGULAR(PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE,
                          SINGULAR: SINGULAR_schemas.Update,
                          service=fastapi.Depends(
                              service_factory.get_SINGULAR_services)):
    """Updates an existing SINGULAR.

    TODO(Add Doc and fix exception text)
    Args:
        PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
        SINGULAR (SINGULAR_schemas.Update): SINGULAR
    """
    SINGULAR = await service.update(PRIMARY_KEY_NAME=PRIMARY_KEY_NAME,
                                    new_SINGULAR=SINGULAR)
    if SINGULAR:
        return SINGULAR
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A SINGULAR with ID: '{PRIMARY_KEY_NAME} was not found.",
    )


@router.get('/{PRIMARY_KEY_NAME}', response_model=SINGULAR_schemas.DB)
async def get_SINGULAR(PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE,
                       service=fastapi.Depends(
                           service_factory.get_SINGULAR_services)):
    """Get a SINGULAR with the provided PRIMARY_KEY_NAME.

    TODO(Add Doc)
    Args:
        PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
    """
    SINGULAR = await service.get_by_id(PRIMARY_KEY_NAME=PRIMARY_KEY_NAME)
    if SINGULAR:
        return SINGULAR
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A SINGULAR with id: '{PRIMARY_KEY_NAME} was not found.",
    )


@router.delete('/{PRIMARY_KEY_NAME}', response_model=SINGULAR_schemas.DB)
async def delete_SINGULAR(PRIMARY_KEY_NAME: PRIMARY_KEY_TYPE,
                          service=fastapi.Depends(
                              service_factory.get_SINGULAR_services)):
    """Deletes the SINGULAR that belongs to the provided PRIMARY_KEY_NAME.

    TODO(Add Doc)
    Args:
        PRIMARY_KEY_NAME (PRIMARY_KEY_TYPE): PRIMARY_KEY_NAME
    """
    return await service.delete(PRIMARY_KEY_NAME=PRIMARY_KEY_NAME)
