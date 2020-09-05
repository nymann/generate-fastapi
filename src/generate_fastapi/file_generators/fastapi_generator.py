"""[summary].

Returns:
    [type]: [description]
"""
from typing import List
import os
import sys

import pydantic
from mako.template import Template
import shutil

from generate_fastapi.schemas import baseschemas
from generate_fastapi.translators.json_translator import JsonTranslator


class FastApiGenerator(pydantic.BaseModel):
    """[summary]."""
    @staticmethod
    def gen_api_files(models, templates_path, target_path, project_name):
        """gen_api_files.

        Args:
            models ([type]): [description]
            templates_path ([type]): [description]
            target_path ([type]): [description]
            project_name ([type]): [description]
        """
        project_dir = '{0}/src/{1}'.format(target_path, project_name)
        _mk_folder_structure(target_path, project_dir, models)

        for model in models:
            _gen_model_route_file(
                model,
                templates_path,
                project_dir,
                project_name,
            )
            _gen_model_domain_files(
                model,
                templates_path,
                project_dir,
                project_name,
            )
            _gen_model_test_files(
                model,
                templates_path,
                target_path,
                project_name,
            )
            _gen_migrations(models, templates_path, target_path, project_name)

        _gen_test_file(models, templates_path, target_path, project_name)
        _gen_common_project_files(models, templates_path, project_dir,
                                  project_name)


def _gen_migrations(models, templates_path, target_path, project_name):
    for model in models:
        template_upgrade_dir = '{0}/migrations/versions/added_routes/upgrade.sql'.format(
            templates_path)
        upgrade_dir = '{0}/migrations/versions/added_{1}/upgrade.sql'.format(
            target_path, model.names.plural_name)

        _gen_model_file(model, template_upgrade_dir, upgrade_dir, project_name)

        template_downgrade_dir = '{0}/migrations/versions/added_routes/downgrade.sql'.format(
            templates_path)
        downgrade_dir = '{0}/migrations/versions/added_{1}/downgrade.sql'.format(
            target_path, model.names.plural_name)

        _gen_model_file(model, template_downgrade_dir, downgrade_dir,
                        project_name)


def _gen_model_file(model, template_path, target_path, project_name):
    if os.path.exists(target_path):
        sys.stdout.write(
            'File {0} already exists. Keeping existing file\n'.format(
                target_path))
        return

    template = Template(filename=template_path)

    primary_key = _get_primary_key(model)

    file_content = template.render(
        model=model,
        PRIMARY_KEY_TYPE=JsonTranslator.translate_typename_to_pytypes(
            primary_key.field_type.name, ),
        PRIMARY_KEY_NAME=primary_key.name,
        PROJECT_NAME=project_name,
        PLURAL_NAME=model.names.plural_name)

    with open(target_path, 'w') as target_file:
        target_file.write(file_content)


def _gen_common_project_files(
    models,
    templates_path,
    project_dir,
    project_name,
):
    _gen_service_factory_file(templates_path, project_dir, project_name,
                              models)

    _gen_base_schemas_file(templates_path, project_dir, project_name, models)

    _gen_project_init_file(templates_path, project_dir, project_name, models)


def _gen_service_factory_file(
    templates_path,
    project_dir,
    project_name,
    models,
):
    template_service_factory_dir = (
        '{0}/src/project/core/service_factory.py.mako').format(templates_path)

    service_factory_dir = '{0}/core/service_factory.py'.format(project_dir)

    _gen_file(
        template_service_factory_dir,
        service_factory_dir,
        project_name,
        models,
    )


def _gen_base_schemas_file(templates_path, project_dir, project_name, models):
    template_base_schemas_dir = (
        '{0}/src/project/domain/template_base_schemas.py.mako'
    ).format(templates_path)
    base_schemas_dir = '{0}/domain/base_schemas.py'.format(project_dir)

    _gen_file(
        template_base_schemas_dir,
        base_schemas_dir,
        project_name,
        models,
    )


def _gen_project_init_file(templates_path, project_dir, project_name, models):
    template_project_init = '{0}/src/project/template_project_init.py.mako'.format(
        templates_path, )
    project_init = '{0}/__init__.py'.format(project_dir)

    if _gen_file(template_project_init, project_init, project_name, models):
        return
    lines = list()
    with open(project_init, "r") as file:
        lines = file.readlines()

    with open(project_init, "w") as write_file:
        for model in models:
            lines = _include_route(file_content=lines,
                                   plural_name=model.names.plural_name,
                                   project_name=project_name)
            write_file.writelines(lines)


def _include_route(file_content: List[str], plural_name: str,
                   project_name: str):
    index = find_suitable_position_in_file(file_content=file_content,
                                           search="from ")
    import_string = 'from {0}.routers import {1}_route\n'.format(
        project_name, plural_name)
    file_content.insert(index, import_string)

    title = plural_name.title()
    route_sentence = '    app.include_router({0}_route.router, tags=["{1}"], prefix="/{0}")\n'.format(
        plural_name, title)
    index = find_suitable_position_in_file(file_content=file_content,
                                           search='app.include_router')
    file_content.insert(index, route_sentence)
    return file_content


def find_suitable_position_in_file(file_content: List[str], search: str):
    for index, line in enumerate(file_content):
        if search not in line:
            continue
        return index
    raise LookupError(
        "Couldn't find an instance of the requested search word: '{0}'.".
        format(search))


def _add_import(import_name: str,
                file_content: List[str],
                from_name: str = None):
    if from_name:
        import_statement = "from {0} ".format(from_name)
    else:
        import_statement = ""
    import_statement = "{0}import {1}".format(import_statement, import_name)
    index = find_suitable_position_in_file(file_content=file_content,
                                           search="import")
    file_content.insert(index, import_statement)
    return file_content


def _gen_test_file(models, templates_path, target_path, project_name):
    template_tests_util_dir = '{0}/tests/utils.py.mako'.format(templates_path)
    tests_utils_dir = '{0}/tests/utils.py'.format(target_path)

    _gen_file(template_tests_util_dir, tests_utils_dir, project_name, models)

    template_conftest_dir = '{0}/tests/conftest.py.mako'.format(templates_path)
    conftest_dir = '{0}/tests/conftest.py'.format(target_path)

    _gen_file(template_conftest_dir, conftest_dir, project_name, models)


def _gen_test_route_init_file(model, templates_path, target_path,
                              project_name):
    template_tests_route_init_dir = '{0}/tests/test_route/__init__.py.mako'.format(
        templates_path, )
    tests_route_init_dir = '{0}/tests/test_{1}/__init__.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(
        model,
        template_tests_route_init_dir,
        tests_route_init_dir,
        project_name,
    )


def _gen_route_bp_test_file(model, templates_path, target_path, project_name):
    template_test_bp_dir = '{0}/tests/test_route/test_basic_positive.py.mako'.format(
        templates_path, )
    test_bp_dir = '{0}/tests/test_{1}/test_basic_positive.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(model, template_test_bp_dir, test_bp_dir, project_name)


def _gen_route_iin_test_file(model, templates_path, target_path, project_name):
    template_test_iin_dir = (
        '{0}/tests/test_route/test_invalid_input_negative.py.mako'
    ).format(templates_path)
    test_iin_dir = '{0}/tests/test_{1}/test_invalid_input_negative.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(model, template_test_iin_dir, test_iin_dir, project_name)


def _gen_route_ep_test_file(model, templates_path, target_path, project_name):
    template_test_ep_dir = (
        '{0}/tests/test_route/test_extended_positive.py.mako'
    ).format(templates_path)
    test_ep_dir = '{0}/tests/test_{1}/test_extended_positive.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(model, template_test_ep_dir, test_ep_dir, project_name)


def _gen_route_dest_test_file(model, templates_path, target_path,
                              project_name):
    template_test_dest_dir = '{0}/tests/test_route/test_destructive.py.mako'.format(
        templates_path, )
    test_dest_dir = '{0}/tests/test_{1}/test_destructive.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(model, template_test_dest_dir, test_dest_dir, project_name)


def _gen_model_test_files(model, templates_path, target_path, project_name):
    _gen_test_route_init_file(model, templates_path, target_path, project_name)

    _gen_route_bp_test_file(model, templates_path, target_path, project_name)

    _gen_route_iin_test_file(model, templates_path, target_path, project_name)

    _gen_route_ep_test_file(model, templates_path, target_path, project_name)

    _gen_route_dest_test_file(model, templates_path, target_path, project_name)


def _gen_model_route_file(model, templates_path, project_dir, project_name):
    template_routers_dir = '{0}/src/project/routers/template_route.py.mako'.format(
        templates_path, )

    routers_dir = '{0}/routers/{1}_route.py'.format(
        project_dir,
        model.names.plural_name,
    )

    _gen_model_file(model, template_routers_dir, routers_dir, project_name)


def _gen_model_service_file(model, templates_path, project_dir, project_name):
    template_services_dir = (
        '{0}/src/project/domain/model/template_services.py.mako'
    ).format(templates_path)

    services_dir = '{0}/domain/{1}/{2}_services.py'.format(
        project_dir,
        model.names.plural_name,
        model.names.singular_name,
    )

    _gen_model_file(model, template_services_dir, services_dir, project_name)


def _gen_model_queries_file(model, templates_path, project_dir, project_name):
    template_queries_dir = (
        '{0}/src/project/domain/model/template_queries.py.mako'
    ).format(templates_path)

    queries_dir = ('{0}/domain/{1}/{2}_queries.py'.format(
        project_dir,
        model.names.plural_name,
        model.names.singular_name,
    ))

    _gen_model_file(model, template_queries_dir, queries_dir, project_name)


def _gen_domain_model_file(model, templates_path, project_dir, project_name):
    template_model_dir = ('{0}/src/project/domain/model/template_model.py.mako'
                          ).format(templates_path)

    model_dir = '{0}/domain/{1}/{2}_model.py'.format(
        project_dir,
        model.names.plural_name,
        model.names.singular_name,
    )

    _gen_model_file(model, template_model_dir, model_dir, project_name)


def _gen_model_schemas_file(model, templates_path, project_dir, project_name):
    template_schemas_dir = (
        '{0}/src/project/domain/model/template_schemas.py.mako'
    ).format(templates_path)

    schemas_dir = ('{0}/domain/{1}/{2}_schemas.py'.format(
        project_dir,
        model.names.plural_name,
        model.names.singular_name,
    ))

    _gen_model_file(model, template_schemas_dir, schemas_dir, project_name)


def _gen_model_domain_files(model, templates_path, project_dir, project_name):
    _gen_model_service_file(model, templates_path, project_dir, project_name)

    _gen_model_queries_file(model, templates_path, project_dir, project_name)

    _gen_domain_model_file(model, templates_path, project_dir, project_name)

    _gen_model_schemas_file(model, templates_path, project_dir, project_name)


def _gen_file(template_path, target_path, project_name, models) -> bool:
    if os.path.exists(target_path):
        sys.stdout.write(
            'File {0} already exists. Keeping existing file\n'.format(
                target_path))
        return False

    template = Template(filename=template_path)

    file_content = template.render(PROJECT_NAME=project_name, models=models)

    with open(target_path, 'w') as target_file:
        target_file.write(file_content)
    return True


def _get_primary_key(model: baseschemas.Model):
    """get_primary_key.

    Args:
        model (baseschemas.Model): [description]

    Returns:
        [type]: [description]
    """
    possible_keys = []
    preferred_types = ['uuid', 'interger']
    for field in model.fields:
        if field.is_primary_key:
            if field.field_type.name in preferred_types:
                return field
            else:
                possible_keys.append(field)

    return possible_keys[0]


def _mk_folder_structure(target_path, project_dir, models):
    """mk_folder_structure.

    Args:
        target_path ([type]): [description]
        project_dir ([type]): [description]
        models ([type]): [description]
    """
    _mk_dir(
        '{0}/src'.format(target_path),
        project_dir,
        '{0}/core'.format(project_dir),
        '{0}/domain'.format(project_dir),
        '{0}/routers'.format(project_dir),
        '{0}/tests'.format(target_path),
        '{0}/migrations'.format(target_path),
        '{0}/migrations/versions'.format(target_path),
    )

    for model in models:
        _mk_dir(
            '{0}/domain/{1}'.format(project_dir, model.names.plural_name),
            '{0}/tests/test_{1}'.format(target_path, model.names.plural_name),
            '{0}/migrations/versions/added_{1}'.format(
                target_path, model.names.plural_name),
        )


def _mk_dir(*target_paths):
    """mk_dir.

    Args:
        target_paths ([type]): [description]
    """
    for target_path in target_paths:
        if os.path.exists(target_path):
            sys.stdout.write(
                ('Folder at: {0} already exists. ' +
                 'Using existing folder instead.\n').format(target_path), )
        else:
            try:
                os.mkdir(target_path)
            except OSError:
                return
            sys.stdout.write('Created folder at: {0}\n'.format(target_path))
