"""[summary].

Returns:
    [type]: [description]
"""

import pydantic


class SqlTranslator(pydantic.BaseModel):
    def translate_to_sqltype_to_common(sqltype):
        translate_dict = {
            'DATE': 'date',
            'TIMESTAMP': 'datetime',
            'UUID': 'uuid',
            'BOOLEAN': 'boolean',
            'INTEGER': 'integer',
            'DOUBLE': 'double',
            'FLOAT': 'float',
            'VARCHAR': 'string',
            'TEXT': 'string'
        }

        return translate_dict.get(sqltype)
