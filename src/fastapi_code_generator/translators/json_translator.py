from dataclasses import field

from fastapi_code_generator.schemas import baseschemas


class JsonTranslator:
    @staticmethod
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
            'string': 'String',
            'uuid': 'UUID',
            'boolean': 'Boolean',
            'integer': 'Integer',
            'double': 'Float',
        }
        return translate_dict.get(type_name)

    @staticmethod
    def translate_field_to_db_dec(field):
        line = [
            'DB.Column({0} = DB.{1}'.format(
                field.name,
                JsonTranslator.translate_db_type(field.type.name),
            ),
        ]
        if field.type.max_length:
            line.append('({0})'.format(field.type.max_length))
        else:
            line.append('()')
        if field.is_primary_key:
            line.append(', primary_key={0}'.format(str(field.is_primary_key)))
        if field.type.default:
            line.append(
                ', default=DB.Text(\"{0}\")'.format(field.type.default), )
        if not field.type.nullable:
            line.append(', nullable={0}'.format(field.type.nullable))
        line.append(')')
        return ''.join(line)

    @staticmethod
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
            'float': 'float'
        }
        return translate_dict.get(type_name)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def translate_sql_type_to_import(type_name):
        """translate_sql_type_to_import.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'DATE': 'datetime',
            'TIMESTAMP': 'datetime',
            'UUID': 'pydantic',
        }
        return translate_dict.get(type_name)
