from dataclasses import field, fields
from os import name

from ${PROJECT_NAME}.core.db import DB

<%! from generate_fastapi.translators.json_translator import JsonTranslator %>

class Model(DB.Model):
    """Model.

    TODO(Add DOC)
    """

    __tablename__ = '${model.names.plural_name}'

    % for field in model.fields:
    ${field.name} = ${JsonTranslator.translate_field_to_db_dec(field)}
    % endfor
