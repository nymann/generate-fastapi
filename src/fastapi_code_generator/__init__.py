""" Init: takes an SQL file and parses it and
generates the required files and folders into the
current working directory.(This will change)
"""
import os
import pathlib
import shutil

import typer

import sql_column_parser
from fastapi_code_generator.schemas import baseschemas
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
    mk_dir(
        '{0}/src'.format(targetpath),
        project_dir,
        '{0}/core'.format(project_dir),
        '{0}/domain'.format(project_dir),
        '{0}/domain/{1}'.format(project_dir, plural_name),
        '{0}/routers'.format(project_dir),
        '{0}/tests'.format(targetpath),
    )


def gen_route_file(templates_path, project_dir, plural_name, replacement_data):
    """gen_route_file.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        plural_name ([type]): [description]
        replacement_data ([type]): [description]
    """
    template_route_dir = os.path.join(templates_path, 'template_route.py')
    replace_in_file(
        template_route_dir,
        '{0}/routers/{1}.py'.format(
            project_dir,
            plural_name,
        ),
        replacement_data,
    )


def gen_db_file(templates_path, project_dir, replacement_data):
    """gen_db_file.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        replacement_data ([type]): [description]
    """
    template_db_dir = os.path.join(templates_path, 'template_db.py')
    replace_in_file(
        template_db_dir,
        '{0}/core/db.py'.format(project_dir),
        replacement_data,
    )


def gen_services_file(
    templates_path,
    project_dir,
    plural_name,
    singular_name,
    replacement_data,
):
    """gen_services_file.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        plural_name ([type]): [description]
        singular_name ([type]): [description]
        replacement_data ([type]): [description]
    """
    template_services_dir = os.path.join(
        templates_path,
        'template_services.py',
    )

    services_dir = '{0}/domain/{1}/{2}_services.py'.format(
        project_dir,
        plural_name,
        singular_name,
    )

    replace_in_file(template_services_dir, services_dir, replacement_data)


def gen_queries_file(
    templates_path,
    project_dir,
    plural_name,
    singular_name,
    replacement_data,
):
    """gen_queries_file.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        plural_name ([type]): [description]
        singular_name ([type]): [description]
        replacement_data ([type]): [description]
    """
    template_queries_dir = os.path.join(templates_path, 'template_queries.py')

    queries_dir = ('{0}/domain/{1}/{2}_queries.py'.format(
        project_dir,
        plural_name,
        singular_name,
    ))

    replace_in_file(template_queries_dir, queries_dir, replacement_data)


def gen_base_schemas_file(templates_path, project_dir, replacement_data):
    """gen_base_schemas_file.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        replacement_data ([type]): [description]
    """
    template_base_schemas_dir = os.path.join(
        templates_path,
        'template_base_schemas.py',
    )
    base_schemas_dir = '{0}/domain/base_schemas.py'.format(project_dir)
    replace_in_file(
        template_base_schemas_dir,
        base_schemas_dir,
        replacement_data,
    )


def gen_model_file(
    templates_path,
    project_dir,
    replacement_data,
    table,
):
    """gen_model_file.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        replacement_data ([type]): [description]
        table ([type]): [description]
    """
    singular_name = table.names.singular_name
    plural_name = table.names.plural_name

    template_model_dir = os.path.join(templates_path, 'template_model.py')
    model_dir = '{0}/domain/{1}/{2}_model.py'.format(
        project_dir,
        plural_name,
        singular_name,
    )

    replace_in_file(template_model_dir, model_dir, replacement_data)
    with open(model_dir, 'a') as model_file:
        model_file.write('\n')
        model_file.write(get_model_declarations(table))


def gen_schemas_file(
    templates_path,
    project_dir,
    plural_name,
    singular_name,
    replacement_data,
):
    """gen_schemas_file.

    Args:
        templates_path ([type]): [description]
        project_dir ([type]): [description]
        plural_name ([type]): [description]
        singular_name ([type]): [description]
        replacement_data ([type]): [description]
    """
    template_schemas_dir = os.path.join(templates_path, 'template_schemas.py')

    schemas_dir = ('{0}/domain/{1}/{2}_schemas.py'.format(
        project_dir,
        plural_name,
        singular_name,
    ))
    replace_in_file(template_schemas_dir, schemas_dir, replacement_data)


def gen_test_files(templates_path, targetpath, table, replacement_data):
    """gen_test_files.

    Args:
        templates_path ([type]): [description]
        targetpath ([type]): [description]
        table ([type]): [description]
        replacement_data ([type]): [description]
    """
    tests_dir = '{0}/tests'.format(targetpath)

    src = os.path.join(templates_path, 'template_test.py')
    target = '{0}/test_{1}.py'.format(tests_dir, table.names.plural_name)
    replace_in_file(src, target, replacement_data)

    src = os.path.join(
        templates_path,
        'template_test_crud.py',
    )
    target = '{0}/test_crud.py'.format(tests_dir)
    replace_in_file(src, target, replacement_data)

    src = os.path.join(
        templates_path,
        'template_conftest.py',
    )
    target = '{0}/conftest.py'.format(tests_dir)
    replace_in_file(src, target, replacement_data)


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
    gen_route_file(templates_path, project_dir, plural_name, replacement_data)

    gen_db_file(templates_path, project_dir, replacement_data)

    gen_services_file(
        templates_path,
        project_dir,
        plural_name,
        singular_name,
        replacement_data,
    )

    gen_queries_file(
        templates_path,
        project_dir,
        plural_name,
        singular_name,
        replacement_data,
    )

    gen_base_schemas_file(templates_path, project_dir, replacement_data)

    gen_model_file(
        templates_path,
        project_dir,
        replacement_data,
        table,
    )

    gen_schemas_file(
        templates_path,
        project_dir,
        plural_name,
        singular_name,
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


def gen_setup_files(templates_path, target_path, replacement_data):
    """gen_setup_files.

    Args:
        templates_path ([type]): [description]
        target_path ([type]): [description]
        replacement_data ([type]): [description]
    """
    template_setup_cfg_dir = os.path.join(templates_path, 'template_setup.cfg')
    setup_cfg_dir = os.path.join(target_path, 'setup.cfg')

    replace_in_file(template_setup_cfg_dir, setup_cfg_dir, replacement_data)

    template_setup_py_dir = os.path.join(templates_path, 'template_setup.py')
    setup_py_dir = os.path.join(target_path, 'setup.py')

    replace_in_file(template_setup_py_dir, setup_py_dir, replacement_data)


def gen_makefiles(templates_path, target_path, replacement_data):
    """gen_makefiles.

    Args:
        templates_path ([type]): [description]
        target_path ([type]): [description]
        replacement_data ([type]): [description]
    """

    template_make_folder = os.path.join(templates_path, 'template_make')
    make_folder = os.path.join(target_path, 'make')

    if os.path.isdir(make_folder):
        print(
            "\"make folder\" at {0} already exists. Keeping old make folder and files"
            .format(make_folder))
    else:
        shutil.copytree(template_make_folder, make_folder)

    template_makefile_dir = os.path.join(templates_path, 'template_Makefile')
    makefile_dir = os.path.join(target_path, 'Makefile')

    replace_in_file(template_makefile_dir, makefile_dir, replacement_data)


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

    replacement_data['PRIMARY_KEY_TYPE'] = translate_sql_type_to_pytypes(
        get_primary_key(table).col_type.name)

    # TODO(FIX ALL PATHS)

    project_dir = '{0}/src/{1}'.format(targetpath, project_name)
    mk_folder_structure(targetpath, project_dir, table.names.plural_name)

    field_format = '\t{0}: {1}\n'
    replacement_data['BASE_FIELDS'] = get_all_colnames_and_typenames_as_string(
        table,
        field_format,
    )

    #field_format = '\t\t\"{}\": test_' + plural_name + '.{},\n'
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

    gen_src_files(
        templates_path,
        project_dir,
        replacement_data,
        table,
    )

    if (gen_additional_files):
        gen_makefiles(templates_path, targetpath, replacement_data)
        gen_setup_files(templates_path, targetpath, replacement_data)

    gen_test_files(templates_path, targetpath, table, replacement_data)


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


def get_column_imports(table: sql_column_parser.schemas.Table):
    """get_column_imports [summary].

    Args:
        table (sql_column_parser.schemas.Table): [description]

    Returns:
        [type]: [description]
    """
    text = []
    for column in table.columns:
        translation = translate_sql_type_to_import(column.col_type.name)
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
                translate_sql_type_to_rand_data(column.col_type.name),
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
            translate_sql_type_to_pytypes(column.col_type.name),
        ))
        declaration.append(line)
    return ''.join(declaration)


def get_model_declarations(table: sql_column_parser.schemas.Table):
    """get_model_declarations [summary].

    Args:
        table (sql_column_parser.schemas.Table): [description]

    Returns:
        [type]: [description]
    """
    declaration = []
    for column in table.columns:
        line = [
            '\t{0} = DB.Column(DB.{1}'.format(
                column.name,
                translate_sql_type(column.col_type.name),
            ),
        ]
        if column.col_type.max_bytesize:
            line.append('({0})'.format(column.col_type.max_bytesize))
        else:
            line.append('()')
        if column.is_primary_key:
            line.append(', primary_key={0}'.format(str(column.is_primary_key)))
        if column.col_type.default:
            line.append(
                ", default=DB.Text(\"{0}\")".format(column.col_type.default), )
        if not column.col_type.nullable:
            line.append(', nullable={0}'.format(column.col_type.nullable))

        line.append(')')
        declaration.append('{0}\n'.format(''.join(line)))
    return ''.join(declaration)


def replace_in_file(src_file_path, target_file_path, replacement_data):
    """replace_in_file [summary].

    Args:
        src_file_path ([type]): [description]
        target_file_path ([type]): [description]
        replacement_data ([type]): [description]
    """

    if os.path.isfile(target_file_path):
        print('File at {0} already exists. Keeping existing file'.format(
            target_file_path))
    else:
        lines = get_file_content(src_file_path)
        with open(target_file_path, 'wt') as output_file:
            for line in lines:
                for word_to_replace, replacement_word in replacement_data.replace_items(
                ):
                    line = line.replace(word_to_replace, replacement_word)
                output_file.write(line)


def get_file_content(src_file_path):
    """get_file_content.

    Args:
        src_file_path ([type]): [description]

    Returns:
        [type]: [description]
    """
    lines = []
    with open(src_file_path, 'rt') as input_file:
        lines = input_file.readlines()
    return lines


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
