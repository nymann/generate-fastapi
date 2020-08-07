""" Init: takes an SQL file and parses it and
generates the required files and folders into the
current working directory.(This will change)
"""
import os
import pathlib

import typer

from fastapi_code_generator.file_generators.fastapi_generator import \
    FastApiGenerator
from fastapi_code_generator.parsers import json_parser


def gen_dirs_and_files(
    json_file,
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

    templates_path = str(
        os.path.join(
            pathlib.Path(__file__).parent.absolute(),
            'mako_templates',
        ))

    models = json_parser.parse_json(json_file)
    FastApiGenerator.gen_api_files(models, templates_path, targetpath,
                                   project_name)


def main(
        json_file,
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
        json_file,
        target_directory,
        project_name,
        gen_setup_files,
    )


def entry_point():
    """entry_point [summary]."""
    typer.run(main)
