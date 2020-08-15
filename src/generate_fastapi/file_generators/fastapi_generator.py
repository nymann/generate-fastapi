"""[summary].

Returns:
    [type]: [description]
"""

import os
import sys

import pydantic
from mako.template import Template
import shutil

from generate_fastapi.schemas import baseschemas
from generate_fastapi.translators.json_translator import JsonTranslator


class FastApiGenerator(pydantic.BaseModel):
    """[summary]."""
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
        _gen_common_project_files(
            models,
            templates_path,
            project_dir,
            project_name,
        )


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
    )

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
        '{0}/src/project/core/service_factory.py').format(templates_path)

    service_factory_dir = '{0}/core/service_factory.py'.format(project_dir)

    _gen_file(
        template_service_factory_dir,
        service_factory_dir,
        project_name,
        models,
    )


def _gen_base_schemas_file(templates_path, project_dir, project_name, models):
    template_base_schemas_dir = (
        '{0}/src/project/domain/template_base_schemas.py'
    ).format(templates_path)
    base_schemas_dir = '{0}/domain/base_schemas.py'.format(project_dir)

    _gen_file(
        template_base_schemas_dir,
        base_schemas_dir,
        project_name,
        models,
    )


def _gen_project_init_file(templates_path, project_dir, project_name, models):
    template_project_init = '{0}/src/project/template_project_init.py'.format(
        templates_path, )
    project_init = '{0}/__init__.py'.format(project_dir)

    _gen_file(template_project_init, project_init, project_name, models)


def _gen_test_file(models, templates_path, target_path, project_name):
    template_tests_util_dir = '{0}/tests/utils.py'.format(templates_path)
    tests_utils_dir = '{0}/tests/utils.py'.format(target_path)

    _gen_file(template_tests_util_dir, tests_utils_dir, project_name, models)

    template_conftest_dir = '{0}/tests/conftest.py'.format(templates_path)
    conftest_dir = '{0}/tests/conftest.py'.format(target_path)

    _gen_file(template_conftest_dir, conftest_dir, project_name, models)


def _gen_test_route_init_file(model, templates_path, target_path,
                              project_name):
    template_tests_route_init_dir = '{0}/tests/test_route/__init__.py'.format(
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
    template_test_bp_dir = '{0}/tests/test_route/test_basic_positive.py'.format(
        templates_path, )
    test_bp_dir = '{0}/tests/test_{1}/test_basic_positive.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(model, template_test_bp_dir, test_bp_dir, project_name)


def _gen_route_iin_test_file(model, templates_path, target_path, project_name):
    template_test_iin_dir = (
        '{0}/tests/test_route/test_invalid_input_negative.py'
    ).format(templates_path)
    test_iin_dir = '{0}/tests/test_{1}/test_invalid_input_negative.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(model, template_test_iin_dir, test_iin_dir, project_name)


def _gen_route_ep_test_file(model, templates_path, target_path, project_name):
    template_test_ep_dir = ('{0}/tests/test_route/test_extended_positive.py'
                            ).format(templates_path)
    test_ep_dir = '{0}/tests/test_{1}/test_extended_positive.py'.format(
        target_path,
        model.names.plural_name,
    )

    _gen_model_file(model, template_test_ep_dir, test_ep_dir, project_name)


def _gen_route_dest_test_file(model, templates_path, target_path,
                              project_name):
    template_test_dest_dir = '{0}/tests/test_route/test_destructive.py'.format(
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
    template_routers_dir = '{0}/src/project/routers/template_route.py'.format(
        templates_path, )

    routers_dir = '{0}/routers/{1}_route.py'.format(
        project_dir,
        model.names.plural_name,
    )

    _gen_model_file(model, template_routers_dir, routers_dir, project_name)


def _gen_model_service_file(model, templates_path, project_dir, project_name):
    template_services_dir = (
        '{0}/src/project/domain/model/template_services.py'
    ).format(templates_path)

    services_dir = '{0}/domain/{1}/{2}_services.py'.format(
        project_dir,
        model.names.plural_name,
        model.names.singular_name,
    )

    _gen_model_file(model, template_services_dir, services_dir, project_name)


def _gen_model_queries_file(model, templates_path, project_dir, project_name):
    template_queries_dir = ('{0}/src/project/domain/model/template_queries.py'
                            ).format(templates_path)

    queries_dir = ('{0}/domain/{1}/{2}_queries.py'.format(
        project_dir,
        model.names.plural_name,
        model.names.singular_name,
    ))

    _gen_model_file(model, template_queries_dir, queries_dir, project_name)


def _gen_domain_model_file(model, templates_path, project_dir, project_name):
    template_model_dir = ('{0}/src/project/domain/model/template_model.py'
                          ).format(templates_path)

    model_dir = '{0}/domain/{1}/{2}_model.py'.format(
        project_dir,
        model.names.plural_name,
        model.names.singular_name,
    )

    _gen_model_file(model, template_model_dir, model_dir, project_name)


def _gen_model_schemas_file(model, templates_path, project_dir, project_name):
    template_schemas_dir = ('{0}/src/project/domain/model/template_schemas.py'
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


def _gen_file(template_path, target_path, project_name, models):
    if os.path.exists(target_path):
        sys.stdout.write(
            'File {0} already exists. Keeping existing file\n'.format(
                target_path))
        return

    template = Template(filename=template_path)

    file_content = template.render(PROJECT_NAME=project_name, models=models)

    with open(target_path, 'w') as target_file:
        target_file.write(file_content)


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
