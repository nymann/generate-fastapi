<%! from generate_fastapi.translators.json_translator import JsonTranslator %>

CREATE TABLE ${model.names.plural_name}(
    % for field in model.fields:
    ${field.name} ${JsonTranslator.translate_field_type_to_sql_type(field.field_type)} ${'' if field.field_type.nullable else 'NOT NULL'},
    %endfor
    PRIMARY KEY (${PRIMARY_KEY_NAME})
)
