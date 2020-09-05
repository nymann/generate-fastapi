"""Init.

Takes an SQL file and parses it and
generates the required files and folders into the
current working directory.(This will change)
"""
import os
import pathlib
import sys
from git import Repo
import typer

from generate_fastapi.file_generators.fastapi_generator import \
        FastApiGenerator
from generate_fastapi.parsers import json_parser
from generate_fastapi.parsers import sql_parser


def gen_dirs_and_files(file: str,
                       targetpath: str,
                       project_name: str,
                       git_repo_url: str = None):
    """gen_dirs_and_files.

    Args:
        json_file ([type]): [description]
        targetpath ([type]): [description]
        project_name ([type]): [description]
        git_repo ([type]): [description]
    """
    if not os.path.isdir(targetpath):
        sys.stdout.write(
            'The target directory does not exist.' +
            'Please try again with a different target path.', )
        return

    if git_repo_url:
        Repo.clone_from(git_repo_url, targetpath)

    templates_path = str(
        os.path.join(
            pathlib.Path(__file__).parent.absolute(), 'mako_templates'))
    models = []
    if file.endswith('.sql'):
        models = sql_parser.parse_sql(file)
    if file.endswith('.json'):
        models = json_parser.parse_json(file)

    print(models)
    FastApiGenerator.gen_api_files(
        models,
        templates_path,
        targetpath,
        project_name,
    )


file_arg: str = typer.Argument(
    ..., help="Path to a SQL upgrade migration or a JSON file")

target_dir_arg: str = typer.Option(".",
                                   help="Path to the target directory",
                                   prompt=True)

project_name_arg: str = typer.Option(...,
                                     help="Your project name fx. 'my_program'")


def main(file: str = file_arg,
         target_directory: str = target_dir_arg,
         project_name: str = project_name_arg,
         git_repo_url: str = typer.Option(None, '--from_repo')):
    """Main entrypoint for the application
    """
    gen_dirs_and_files(file=file,
                       targetpath=target_directory,
                       project_name=project_name,
                       git_repo_url=git_repo_url)


def entry_point():
    """entry_point [summary]."""
    typer.run(main)
