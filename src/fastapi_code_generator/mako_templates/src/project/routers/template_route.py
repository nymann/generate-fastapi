"""Endpoints starting with /${model.names.plural_name}/ are defined here.

This module contains all API endpoints which path contains '/${model.names.plural_name}/'.
Not that no "business-logic" is defined in here, we simply pass in onto
the ${model.names.singular_name} service from the `service_factory`, by doing it this way
the controller only knows which methods it can call in ${model.names.singular_name} Service
but nothing about the database.
"""

import fastapi
import pydantic
from starlette import status

from ${PROJECT_NAME}.core import security, service_factory
from ${PROJECT_NAME}.domain.${model.names.plural_name} import (
    ${model.names.singular_name}_schemas)

router = fastapi.APIRouter()

% if any(route.name == 'GetList' and route.include for route in model.routes):
@router.get('/', response_model=${model.names.singular_name}_schemas.Paginated)
async def get_${model.names.plural_name}(page_size: pydantic.conint(ge=1, le=100) = 20,
                     page: pydantic.conint(ge=1) = 1,
                     service=fastapi.Depends(
                         service_factory.get_${model.names.singular_name}_services)):
    """Get a paginated list of ${model.names.plural_name}.

    TODO(Add Doc)
    Args:
        page_size (pydantic.conint(ge=1, le=100)): page_size
        page (pydantic.conint(ge=1)): page
        service:
    """
    return await service.get_list(page=page, page_size=page_size)
%endif

% if any((route.name == 'Post' and route.include) for route in model.routes):
@router.post('/',
             response_model=${model.names.singular_name}_schemas.DB,
             status_code=status.HTTP_201_CREATED)
async def add_${model.names.singular_name}(${model.names.singular_name}: ${model.names.singular_name}_schemas.Create,
                       service=fastapi.Depends(
                           service_factory.get_${model.names.singular_name}_services)):
    """Create a new ${model.names.singular_name}.

    TODO(Add Doc)
    Args:
        ${model.names.singular_name} (${model.names.singular_name}_schemas.Create): ${model.names.singular_name}
    """
    return await service.create(${model.names.singular_name}=${model.names.singular_name})
%endif

% if any((route.name == 'Update' and route.include) for route in model.routes):
@router.put('/{${PRIMARY_KEY_NAME}}', response_model=${model.names.singular_name}_schemas.DB)
async def update_${model.names.singular_name}(${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE},
                          ${model.names.singular_name}: ${model.names.singular_name}_schemas.Update,
                          service=fastapi.Depends(
                              service_factory.get_${model.names.singular_name}_services)):
    """Updates an existing ${model.names.singular_name}.

    TODO(Add Doc and fix exception text)
    Args:
        ${PRIMARY_KEY_NAME} (${PRIMARY_KEY_TYPE}): ${PRIMARY_KEY_NAME}
        ${model.names.singular_name} (${model.names.singular_name}_schemas.Update): ${model.names.singular_name}
    """
    ${model.names.singular_name} = await service.update(${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME},
                                    new_${model.names.singular_name}=${model.names.singular_name})
    if ${model.names.singular_name}:
        return ${model.names.singular_name}
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A ${model.names.singular_name} with ID: '{${PRIMARY_KEY_NAME}} was not found.",
    )
%endif

% if any((route.name == 'GetById' and route.include) for route in model.routes):
@router.get('/{${PRIMARY_KEY_NAME}}', response_model=${model.names.singular_name}_schemas.DB)
async def get_${model.names.singular_name}(${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE},
                       service=fastapi.Depends(
                           service_factory.get_${model.names.singular_name}_services)):
    """Get a ${model.names.singular_name} with the provided ${PRIMARY_KEY_NAME}.

    TODO(Add Doc)
    Args:
        ${PRIMARY_KEY_NAME} (${PRIMARY_KEY_TYPE}): ${PRIMARY_KEY_NAME}
    """
    ${model.names.singular_name} = await service.get_by_id(${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
    if ${model.names.singular_name}:
        return ${model.names.singular_name}
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A ${model.names.singular_name} with id: '{${PRIMARY_KEY_NAME}} was not found.",
    )
% endif

% if any((route.name == 'DeleteById' and route.include) for route in model.routes):
@router.delete('/{${PRIMARY_KEY_NAME}}', response_model=${model.names.singular_name}_schemas.DB)
async def delete_${model.names.singular_name}(${PRIMARY_KEY_NAME}: ${PRIMARY_KEY_TYPE},
                          service=fastapi.Depends(
                              service_factory.get_${model.names.singular_name}_services)):
    """Deletes the ${model.names.singular_name} that belongs to the provided ${PRIMARY_KEY_NAME}.

    TODO(Add Doc)
    Args:
        ${PRIMARY_KEY_NAME} (${PRIMARY_KEY_TYPE}): ${PRIMARY_KEY_NAME}
    """
    return await service.delete(${PRIMARY_KEY_NAME}=${PRIMARY_KEY_NAME})
%endif
