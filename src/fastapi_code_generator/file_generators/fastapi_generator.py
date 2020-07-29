import os
import shutil

import sql_column_parser
from fastapi_code_generator.translators.sql_translator import SqlTranslator


class FastApiGenerator:
    def gen_route_file(templates_path, project_dir, plural_name,
                       replacement_data):
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
        template_queries_dir = os.path.join(templates_path,
                                            'template_queries.py')

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
        template_schemas_dir = os.path.join(templates_path,
                                            'template_schemas.py')

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

    def gen_setup_files(templates_path, target_path, replacement_data):
        """gen_setup_files.

        Args:
            templates_path ([type]): [description]
            target_path ([type]): [description]
            replacement_data ([type]): [description]
        """
        template_setup_cfg_dir = os.path.join(templates_path,
                                              'template_setup.cfg')
        setup_cfg_dir = os.path.join(target_path, 'setup.cfg')

        replace_in_file(template_setup_cfg_dir, setup_cfg_dir,
                        replacement_data)

        template_setup_py_dir = os.path.join(templates_path,
                                             'template_setup.py')
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

        template_makefile_dir = os.path.join(templates_path,
                                             'template_Makefile')
        makefile_dir = os.path.join(target_path, 'Makefile')

        replace_in_file(template_makefile_dir, makefile_dir, replacement_data)


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
                SqlTranslator.translate_sql_type(column.col_type.name),
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
