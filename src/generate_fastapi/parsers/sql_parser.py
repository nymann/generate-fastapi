import inflect
import re

from generate_fastapi.schemas import baseschemas
from generate_fastapi.translators.sql_translator import SqlTranslator


def parse_sql(path):
    """parse_json.

    Args:
        path ([type]): [description]

    Returns:
        [type]: [description]
    """
    model_statements = []
    with open(file=path, mode="r") as f:
        statements = f.read().split(";")
        for statement in statements:
            statement = statement.strip("\n")
            model_statements.append(statement)

    return _parse_statements(model_statements)


def _parse_statements(statements):
    pattern = re.compile(r"^CREATE TABLE\s*(\S*)\s* \(")
    models = []
    for statement in statements:
        create_table_statement = pattern.search(statement)
        if create_table_statement is None:
            continue
        plural_name = pattern.match(statement).group(1)
        engine = inflect.engine()
        singular_name = engine.singular_noun(plural_name)

        models.append(
            baseschemas.Model(
                fields=_parse_fields(statement),
                routes=[
                    baseschemas.Route(name='GetList', include=True),
                    baseschemas.Route(name='GetById', include=True),
                    baseschemas.Route(name='Post', include=True),
                    baseschemas.Route(name='Update', include=True),
                    baseschemas.Route(name='DeleteById', include=True),
                ],
                names=baseschemas.Names(singular_name=singular_name,
                                        plural_name=plural_name),
            ))

    return models


def _parse_fields(create_table_statement):
    field_texts = []
    primary_key_names = []
    for line in create_table_statement.split("\n")[1:-1]:
        line = line.strip()
        line = line.strip(",")
        if _is_not_field(line=line):
            if _parse_primary_keys(line):
                primary_key_names.extend(_parse_primary_keys(line))
            continue
        field_texts.append(line)

    fields = []
    for field_text in field_texts:
        fields.append(_parse_field(field_text, primary_key_names))

    return fields


def _parse_field(field_text, primary_key_names):
    """parse_column.
        Args:
            column_text:
        """
    words = field_text.split(" ")
    field_name = words[0]
    type_name = words[1]

    default = None
    nullable = True

    is_primary_key = field_name in primary_key_names

    if len(words) > 2:
        text = " ".join(words[2:])
        nullable = _is_nullable(text)
        default = _parse_default_value(text)

    max_length = _parse_max_length(type_name)
    if max_length is not None:
        type_name = type_name.split("(")[0]

    field_type = baseschemas.FieldType(
        name=SqlTranslator.translate_to_sqltype_to_common(type_name),
        nullable=nullable,
        max_length=max_length,
        min_length=None,
        default=default)
    return baseschemas.Field(name=field_name,
                             field_type=field_type,
                             is_primary_key=is_primary_key)


def _is_not_field(line: str) -> bool:
    """is_not_column.
    Args:
        line (str): line
    Returns:
        bool:
    """
    BLACKLIST = ["primary", "unique"]
    line = line.lower()
    return any(line.startswith(word) for word in BLACKLIST)


def _is_nullable(line: str) -> bool:
    """_is_nullable.
    Args:
        line (str): line
    Returns:
        bool:
    """
    return "NOT NULL" not in line.upper()


def _parse_max_length(type_name: str):
    """_parse_max_bytesize.
    Args:
        type_name (str): type_name
    """
    pattern = re.compile(r"\((\d*)\)")
    match = pattern.search(type_name)
    if match is None:
        return None
    else:
        max_bytesize = match.group(1)
        return max_bytesize


def _parse_default_value(line):
    """_parse_default_value.
    Args:
        line:
    """
    default_text = line.split("DEFAULT")
    if len(default_text) == 1:
        return None
    else:
        return default_text[1].split(" ")[1]


def _parse_primary_keys(line):
    """_parse_primary_keys.
    Args:
        line:
    """
    if not line.upper().startswith("PRIMARY"):
        return
    pattern = re.compile(r"\((\S*\,*)\)")
    match = pattern.search(line).group(1)
    match = match.replace(" ", "")
    keys = match.split(",")

    return keys
