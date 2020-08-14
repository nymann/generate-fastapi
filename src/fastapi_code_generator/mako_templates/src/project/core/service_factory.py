% for model in models:
from ${PROJECT_NAME}.domain.${model.names.plural_name} import ${model.names.singular_name}_queries
from ${PROJECT_NAME}.domain.${model.names.plural_name}.${model.names.singular_name}_services import Service
%endfor

% for model in models:
def get_${model.names.singular_name}_services() -> Service:
    """Gets an instance of `Service`.

    Routers that makes dependency injection

    Args:

    Returns:
        ${model.names.singular_name}_services.Service:
    """
    return Service(${model.names.singular_name}_queries.Queries())

%endfor
