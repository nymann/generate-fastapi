import pytest
from generate_fastapi.parsers import json_parser
import os
import generate_fastapi


def test_is_folders_created(tmpdir_factory):
    tmp_dir = tmpdir_factory.mktemp('data')
    generate_fastapi.gen_dirs_and_files('examples/example.json', tmp_dir,
                                        'test_api', '')

    assert os.path.exists(tmp_dir / 'src')
    assert os.path.exists(tmp_dir / 'src' / 'test_api')
    assert os.path.exists(tmp_dir / 'src' / 'test_api' / 'core')
    assert os.path.exists(tmp_dir / 'src' / 'test_api' / 'domain')
    assert os.path.exists(tmp_dir / 'src' / 'test_api' / 'domain' / 'users')
    assert os.path.exists(tmp_dir / 'src' / 'test_api' / 'routers')
    assert os.path.exists(tmp_dir / 'src' / 'test_api' / 'core')

    assert os.path.exists(tmp_dir / 'tests')
    assert os.path.exists(tmp_dir / 'tests' / 'test_users')


def test_model_files_created(tmpdir_factory):
    tmp_dir = tmpdir_factory.mktemp('data')
    generate_fastapi.gen_dirs_and_files('examples/example.json', tmp_dir,
                                        'test_api', '')

    model_dir = tmp_dir / 'src' / 'test_api' / 'domain' / 'users'

    assert os.path.isfile((model_dir / 'user_model.py'))
    assert os.path.isfile(model_dir / 'user_queries.py')
    assert os.path.isfile(model_dir / 'user_schemas.py')
    assert os.path.isfile(model_dir / 'user_services.py')


def test_test_files_created(tmpdir_factory):
    tmp_dir = tmpdir_factory.mktemp('data')
    generate_fastapi.gen_dirs_and_files('examples/example.json', tmp_dir,
                                        'test_api', '')

    tests_dir = tmp_dir / 'tests'
    assert os.path.isfile(tests_dir / 'conftest.py')
    assert os.path.isfile(tests_dir / 'utils.py')

    tests_model_dir = tests_dir / 'test_users'
    assert os.path.isfile((tests_model_dir / 'test_basic_positive.py'))
    assert os.path.isfile(tests_model_dir / 'test_destructive.py')
    assert os.path.isfile(tests_model_dir / 'test_extended_positive.py')
    assert os.path.isfile(tests_model_dir / 'test_invalid_input_negative.py')
