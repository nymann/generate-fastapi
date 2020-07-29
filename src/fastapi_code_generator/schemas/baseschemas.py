""" Baseschemas.

Returns:
    [type]: [description]
"""

from typing import Dict

import sql_column_parser


class ReplacementData(Dict):
    """ReplacementData.

    Returns:
        [type]: [description]
    """

    replacement_dict: Dict[str, str]

    def __init__(self, project_name, table: sql_column_parser.schemas.Table):
        """__init__.

        Args:
            project_name ([type]): [description]
            table (sql_column_parser.schemas.Table): [description]
        """
        primary_key_column = get_primary_key(table)
        self.replacement_dict = {
            'SINGULAR': table.names.singular_name,
            'PLURAL': table.names.plural_name,
            'PROJECT_NAME': project_name,
            'PRIMARY_KEY_NAME': primary_key_column.name,
        }

    def __getitem__(self, key):
        """__getitem__.

        Args:
            key ([type]): [description]

        Returns:
            [type]: [description]
        """
        print(key + " " + self.replacement_dict[key])
        return self.replacement_dict[key]

    def __setitem__(self, word_to_replace, replacement_word):
        """__setitem__.

        Args:
            word_to_replace ([type]): [description]
            replacement_word ([type]): [description]
        """
        self.replacement_dict[word_to_replace] = replacement_word

    def replace_items(self):
        """items.

        Returns:
            [type]: [description]
        """
        return self.replacement_dict.items()


def get_primary_key(table: sql_column_parser.schemas.Table):
    """get_primary_key.

    Args:
        table (sql_column_parser.schemas.Table): [description]

    Returns:
        [type]: [description]
    """
    possible_keys = []
    preferred_types = ['UUID', 'INTEGER']
    for column in table.columns:
        if column.is_primary_key:
            if column.col_type.name in preferred_types:
                return column
            else:
                possible_keys.append(column)

    return possible_keys[0]
