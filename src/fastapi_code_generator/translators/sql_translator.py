class SqlTranslator:
    @staticmethod
    def translate_sql_type(type_name):
        """translate_sql_type.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'DATE': 'Date',
            'TIMESTAMP': 'DateTime',
            'VARCHAR': 'String',
            'TEXT': 'String',
            'UUID': 'UUID',
            'BOOLEAN': 'Boolean',
            'INTEGER': 'Integer',
            'DOUBLE': 'Float',
        }
        return translate_dict.get(type_name)

    @staticmethod
    def translate_sql_type_to_pytypes(type_name):
        """translate_sql_type_to_pytypes.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'DATE': 'datetime.date',
            'TIMESTAMP': 'datetime.datetime',
            'VARCHAR': 'str',
            'TEXT': 'str',
            'UUID': 'pydantic.UUID4',
            'BOOLEAN': 'bool',
            'INTEGER': 'int',
            'DOUBLE': 'float',
        }
        return translate_dict.get(type_name)

    @staticmethod
    def translate_sql_type_to_rand_data(type_name):
        """translate_sql_type_to_rand_data.

        Args:
            type_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        translate_dict = {
            'DATE': 'rand_date()',
            'TIMESTAMP': 'rand_datetime()',
            'VARCHAR': 'random(8)',
            'TEXT': 'random(20)',
            'UUID': 'uuid.uuid4()',
            'BOOLEAN': 'rand_bool()',
            'INTEGER': 'random.randint(0,200)',
            'DOUBLE': 'random.uniform(0,200)',
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
