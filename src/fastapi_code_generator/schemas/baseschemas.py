import sql_column_parser


class ReplacementData():
    replacement_dict = {}

    def __init__(self, project_name, table: sql_column_parser.schemas.Table):
        primary_key_column = get_primary_key(table)
        self.replacement_dict = {
            'SINGULAR': table.names.singular_name,
            'PLURAL': table.names.plural_name,
            'PROJECT_NAME': project_name,
            'PRIMARY_KEY_NAME': primary_key_column.name,
            'PRIMARY_KEY_TYPE': primary_key_column.col_type.name,
        }

    def __getitem__(self, key):
        return self.replacement_dict[key]

    def __setitem__(self, word_to_replace, replacement_word):
        self.replacement_dict[word_to_replace] = replacement_word

    def items(self):
        return self.replacement_dict.items()


def get_primary_key(table: sql_column_parser.schemas.Table):
    possible_keys = []
    preferred_types = ['UUID', 'INTEGER']
    for column in table.columns:
        if column.is_primary_key:
            if column.col_type.name in preferred_types:
                return column
            else:
                possible_keys.append(column)

    return possible_keys[0]
