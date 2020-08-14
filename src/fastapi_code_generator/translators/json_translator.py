"""[summary].

Returns:
    [type]: [description]
"""

import pydantic


class JsonTranslator(pydantic.BaseModel):
    """[summary]."""
    def translate_db_type(type_name):
        """translate_db_type.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'date': 'Date',
            'datetime': 'DateTime',
            'string': 'String',
            'uuid': 'UUID',
            'boolean': 'Boolean',
            'integer': 'Integer',
            'double': 'Float',
        }
        return translate_dict.get(type_name)

    def translate_field_to_db_dec(field):
        """translate_field_to_db_dec.

        Args:
            field ([type]): [description]

        Returns:
            [type]: [description]
        """
        line = [
            'DB.Column({0} = DB.{1}'.format(
                field.name,
                JsonTranslator.translate_db_type(field.field_type.name),
            ),
        ]
        if field.field_type.max_length:
            line.append('({0})'.format(field.field_type.max_length))
        else:
            line.append('()')
        if field.is_primary_key:
            line.append(', primary_key={0}'.format(str(field.is_primary_key)))
        if field.field_type.default:
            line.append(
                ', default=DB.Text(\"{0}\")'.format(
                    field.field_type.default), )
        if not field.field_type.nullable:
            line.append(', nullable={0}'.format(field.field_type.nullable))
        line.append(')')
        return ''.join(line)

    def translate_field_type_to_sql_type(field_type):
        if field_type.name == 'string':
            if field_type.max_length:
                return 'VARCHAR({0})'.format(field_type.max_length)
            else:
                return 'TEXT'
        else:
            translate_dict = {
                'date': 'DATE',
                'datetime': 'TIMESTAMP',
                'uuid': 'UUID',
                'boolean': 'BOOLEAN',
                'integer': 'INTEGER',
                'double': 'DOUBLE',
                'float': 'FLOAT',
            }
            if field_type.max_length:
                return '{0}({1})'.format(translate_dict.get(field_type.name),
                                         field_type.max_length)
            else:
                return translate_dict.get(field_type.name)

    def translate_typename_to_pytypes(type_name):
        """translate_sql_type_to_pytypes.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'date': 'datetime.date',
            'datetime': 'datetime.datetime',
            'string': 'str',
            'uuid4': 'pydantic.UUID4',
            'uuid': 'pydantic.UUID4',
            'boolean': 'bool',
            'integer': 'int',
            'double': 'float',
            'float': 'float',
        }
        return translate_dict.get(type_name)

    def translate_typename_to_rand_data(type_name):
        """translate_typename_to_rand_data.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'date': 'utils.random_date(2020, 2050)',
            'datetime': 'utils.random_datetime(2020, 2050)',
            'string': 'utils.random_string(8)',
            'uuid4': 'uuid.uuid4()',
            'uuid': 'uuid.uuid4()',
            'boolean': 'utils.random_boolean()',
            'integer': 'random.randint(0,200)',
            'double': 'random.uniform(0,200)',
            'float': 'random.uniform(0,200)',
        }
        return translate_dict.get(type_name)

    def translate_pytype_to_rand_data(type_name):
        """translate_typename_to_rand_data.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'datetime.date': 'utils.random_date(2020, 2050)',
            'datetime.datetime': 'utils.random_datetime(2020, 2050)',
            'str': 'utils.random_string(8)',
            'pydantic.UUID4': 'uuid.uuid4()',
            'bool': 'utils.random_boolean()',
            'int': 'random.randint(0,200)',
            'float': 'random.uniform(0,200)',
        }
        return translate_dict.get(type_name)

    def translate_typename_to_invalid_data(type_name):
        """translate_typename_to_rand_data.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'date': '\"notadate\"',
            'datetime': '\"notadatetime\"',
            'string': 'utils.random_string(8)',
            'uuid4': 'uuid.uuid4()',
            'uuid': 'uuid.uuid4()',
            'boolean': '\"notaboolean\"',
            'integer': '\"notainteger\"',
            'double': '\"notadouble\"',
            'float': '\"notafloat\"',
        }
        return translate_dict.get(type_name)
