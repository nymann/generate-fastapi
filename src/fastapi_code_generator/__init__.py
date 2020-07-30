""" Init: takes an SQL file and parses it and
generates the required files and folders into the
current working directory.(This will change)
"""
import os
import pathlib
import shutil
from os import replace

import sql_column_parser
import typer
from fastapi_code_generator.file_generators.fastapi_generator import \
    FastApiGenerator
from fastapi_code_generator.schemas import baseschemas
from fastapi_code_generator.translators.sql_translator import SqlTranslator
from sql_column_parser import schemas


def mk_dir(*targetpaths):
    """mk_dir.

    Args:
        targetpath ([type]): [description]
    """
    for targetpath in targetpaths:
        if not os.path.isdir(targetpath):
            try:
                print('Created folder at: {0}'.format(targetpath))
                os.mkdir(targetpath)
            except OSError:
                return
        else:
            print(
                'Folder at: {0} already exists. Using existing folder instead.'
                .format(targetpath))


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


def mk_folder_structure(targetpath, project_dir, plural_name):
    """mk_folder_structure.

    Args:
        targetpath ([type]): [description]
        project_dir ([type]): [description]
        plural_name ([type]): [description]
    """
    FastApiGenerator.mk_dir(
        '{0}/src'.format(targetpath),
        project_dir,
        '{0}/core'.format(project_dir),
        '{0}/domain'.format(project_dir),
        '{0}/domain/{1}'.format(project_dir, plural_name),
        '{0}/routers'.format(project_dir),
        '{0}/tests'.format(targetpath),
    )


def gen_src_files(
    templates_path,
    project_dir,
    replacement_data,
    table: sql_column_parser.schemas.Table,
):
    """gen_src_files.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        replacement_data ([type]): [description]
        table (sql_column_parser.schemas.Table): [description]
    """
    singular_name = table.names.singular_name
    plural_name = table.names.plural_name
    FastApiGenerator.gen_route_file(templates_path, project_dir, plural_name,
                                    replacement_data)

    FastApiGenerator.gen_db_file(templates_path, project_dir, replacement_data)

    FastApiGenerator.gen_config_loader_file(
        templates_path,
        project_dir,
        replacement_data,
    )

    FastApiGenerator.gen_services_file(
        templates_path,
        project_dir,
        plural_name,
        singular_name,
        replacement_data,
    )

    FastApiGenerator.gen_queries_file(
        templates_path,
        project_dir,
        plural_name,
        singular_name,
        replacement_data,
    )

    FastApiGenerator.gen_base_schemas_file(templates_path, project_dir,
                                           replacement_data)

    FastApiGenerator.gen_model_file(
        templates_path,
        project_dir,
        replacement_data,
        table,
    )

    FastApiGenerator.gen_schemas_file(
        templates_path,
        project_dir,
        plural_name,
        singular_name,
        replacement_data,
    )

    FastApiGenerator.gen_project_init_file(
        templates_path,
        project_dir,
        replacement_data,
    )


def get_table(sql_file):
    """get_table.

    Args:
        sql_file ([type]): [description]

    Returns:
        [type]: [description]
    """
    parser = sql_column_parser.Parser(sql_file)
    return parser.parse()


def gen_dirs_and_files(
    sql_file,
    targetpath,
    project_name,
    gen_additional_files,
):
    """gen_dirs_and_files.

    Args:
        sql_file ([type]): [description]
        targetpath ([type]): [description]
        project_name ([type]): [description]
        gen_additional_files ([type]): [description]
    """
    if not os.path.isdir(targetpath):
        print(
            "The target directory does not exist. Please try again with a different target path."
        )
        return

    templates_path = os.path.join(
        pathlib.Path(__file__).parent.absolute(),
        'templates',
    )

    table = get_table(sql_file)

    replacement_data = baseschemas.ReplacementData(project_name, table)

    replacement_data[
        'PRIMARY_KEY_TYPE'] = SqlTranslator.translate_sql_type_to_pytypes(
            get_primary_key(table).col_type.name)

    # TODO(FIX ALL PATHS)

    project_dir = '{0}/src/{1}'.format(targetpath, project_name)
    mk_folder_structure(targetpath, project_dir, table.names.plural_name)

    replacement_data = add_additional_text_to_replacement_data(
        table, replacement_data)

    gen_src_files(
        templates_path,
        project_dir,
        replacement_data,
        table,
    )

    if (gen_additional_files):
        FastApiGenerator.gen_makefiles(templates_path, targetpath,
                                       replacement_data)
        FastApiGenerator.gen_setup_files(templates_path, targetpath,
                                         replacement_data)

    FastApiGenerator.gen_test_files(templates_path, targetpath, table,
                                    replacement_data)


def add_additional_text_to_replacement_data(table, replacement_data):
    field_format = '\t{0}: {1}\n'
    replacement_data['BASE_FIELDS'] = get_all_colnames_and_typenames_as_string(
        table,
        field_format,
    )

    field_format = '\t\t\"{0}\": test_{1}.{2},\n'.format(
        '{0}',
        table.names.plural_name,
        '{1}',
    )
    replacement_data['RANDOM_MOCKDATA'] = create_mock_data(table, field_format)

    field_format = ', {0}: {1}'
    replacement_data['COMMA_SEPARATED_FIELDS'] = (
        get_all_colnames_and_typenames_as_string(
            table,
            field_format,
        ))

    field_format = '{0}={1},'
    replacement_data['COMMA_SEPARATED_COLNAMES'] = get_colnames_twice(
        table,
        field_format,
    )[:-1]

    return replacement_data


def get_column_imports(table: sql_column_parser.schemas.Table):
    """get_column_imports [summary].

    Args:
        table (sql_column_parser.schemas.Table): [description]

    Returns:
        [type]: [description]
    """
    text = []
    for column in table.columns:
        translation = SqlTranslator.translate_sql_type_to_import(
            column.col_type.name)
        if translation is not None:
            text.append('import {0}\n'.format(translation))
    return ''.join(text)


def get_colnames_twice(
    table: sql_column_parser.schemas.Table,
    field_format: str,
):
    """get_colnames_twice [summary].

    Args:
        table (sql_column_parser.schemas.Table): [description]
        field_format (str): [description]

    Returns:
        [type]: [description]
    """
    text = []
    for column in table.columns:
        if column.is_primary_key:
            continue
        text.append(field_format.format(column.name, column.name))
    return ''.join(text)


def create_mock_data(table: sql_column_parser.schemas.Table,
                     field_format: str):
    """create_mock_data [summary].

    Args:
        table (sql_column_parser.schemas.Table): [description]
        field_format (str): [description]

    Returns:
        [type]: [description]
    """
    text = []
    for column in table.columns:
        if column.is_primary_key:
            continue
        text.append(
            field_format.format(
                column.name,
                SqlTranslator.translate_sql_type_to_rand_data(
                    column.col_type.name),
            ))
    return ''.join(text)


def get_all_colnames_and_typenames_as_string(
    table: sql_column_parser.schemas.Table,
    field_format: str,
):
    """get_all_colnames_and_typenames_as_string [summary].

    Args:
        table (sql_column_parser.schemas.Table): [description]
        field_format (str): [description]

    Returns:
        [type]: [description]
    """
    declaration = []
    for column in table.columns:
        if column.is_primary_key and column.col_type.default:
            continue
        line = (field_format.format(
            column.name,
            SqlTranslator.translate_sql_type_to_pytypes(column.col_type.name),
        ))
        declaration.append(line)
    return ''.join(declaration)


def main(
        sql_file,
        target_directory,
        project_name,
        gen_setup_files: bool = typer.Option(False, '--gen_setup_files'),
):
    """Run the main method.

    Args:
        sql_file ([type]): [description]
        target_directory ([type]): [description]
        project_name ([type]): [description]
        gen_setup_files (bool): [description]. Defaults to typer_option.
    """
    gen_dirs_and_files(
        sql_file,
        target_directory,
        project_name,
        gen_setup_files,
    )


def entry_point():
    """entry_point [summary]."""
    typer.run(main)
