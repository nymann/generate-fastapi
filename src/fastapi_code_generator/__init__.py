""" Init: takes an SQL file and parses it and
generates the required files and folders into the
current working directory.(This will change)
"""
import os
import pathlib
import sys
from typing import Text

import sql_column_parser
from sql_column_parser import schemas
import typer


def mk_dir(targetpath):
    try:
        os.mkdir(targetpath)
    except OSError:
        print("Fail")
    else:
        print("Success")


def get_primary_key(table: sql_column_parser.schemas.Table):
    possible_keys = []
    prefered_types = ["UUID", "INTEGER"]
    for column in table.columns:
        if column.is_primary_key:
            if column.col_type.name in prefered_types:
                return column
            else:
                possible_keys.append(column)

    return possible_keys[0]


def gen_dirs_and_files(file, targetpath, project_name):

    cur_directory = pathlib.Path(__file__).parent.absolute()
    templates_path = os.path.join(cur_directory, "templates")

    parser = sql_column_parser.Parser(file)
    table = parser.parse()

    singular_name = table.names.singular_name
    plural_name = table.names.plural_name

    primary_key_column = get_primary_key(table)
    primary_key_name = primary_key_column.name
    primary_key_type = translate_sql_type_to_pytypes(
        primary_key_column.col_type.name)

    replacement_dict = {
        "SINGULAR": singular_name,
        "PLURAL": plural_name,
        "PROJECT_NAME": project_name,
        "PRIMARY_KEY_NAME": primary_key_name,
        "PRIMARY_KEY_TYPE": primary_key_type
    }

    #TODO(FIX ALL PATHS)

    project_dir = targetpath + "/src/" + project_name
    mk_dir(targetpath + "/src")
    mk_dir(project_dir)
    mk_dir(project_dir + "/core")
    mk_dir(project_dir + "/domain")
    mk_dir(project_dir + "/domain/" + plural_name)
    mk_dir(project_dir + "/routers")
    mk_dir(targetpath + "/tests")

    template_route_dir = os.path.join(templates_path, "template_route.py")
    replace_in_file(template_route_dir,
                    project_dir + "/routers/" + plural_name + ".py",
                    replacement_dict)

    template_db_dir = os.path.join(templates_path, "template_db.py")
    replace_in_file(template_db_dir, project_dir + "/core/db.py",
                    replacement_dict)

    template_services_dir = os.path.join(templates_path, "template_services.py")
    services_dir = f"{project_dir}/domain/{plural_name}" + \
                     f"/{singular_name}_services.py"
    replace_in_file(template_services_dir, services_dir, replacement_dict)

    template_queries_dir = os.path.join(templates_path, "template_queries.py")
    queries_dir = f"{project_dir}/domain/{plural_name}/{singular_name}_queries.py"
    replace_in_file(template_queries_dir, queries_dir, replacement_dict)

    template_base_schemas_dir = os.path.join(templates_path,
                                             "template_base_schemas.py")
    base_schemas_dir = f"{project_dir}/domain/base_schemas.py"
    replace_in_file(template_base_schemas_dir, base_schemas_dir,
                    replacement_dict)

    template_model_dir = os.path.join(templates_path, "template_model.py")
    model_dir = f"{project_dir}/domain/{plural_name}/{singular_name}_model.py"
    replace_in_file(template_model_dir, model_dir, replacement_dict)

    replacement_dict["BASE_FIELDS"] = get_schemas_base_declaration(table)
    template_schemas_dir = os.path.join(templates_path, "template_schemas.py")
    schemas_dir = f"{project_dir}/domain/{plural_name}/{singular_name}_schemas.py"
    replace_in_file(template_schemas_dir, schemas_dir, replacement_dict)

    model_file = open(model_dir, "a")
    model_file.write("\n")
    model_file.write(get_model_declarations(table))

    print(get_schemas_base_declaration(table))


def translate_sql_type(type_name):
    translate_dict = {
        "DATE": "Date",
        "TIMESTAMP": "Datetime",
        "VARCHAR": "String",
        "TEXT": "String",
        "UUID": "UUID"
    }
    return translate_dict.get(type_name)


def translate_sql_type_to_pytypes(type_name):
    translate_dict = {
        "DATE": "datetime.date",
        "TIMESTAMP": "datetime.datetime",
        "VARCHAR": "str",
        "TEXT": "str",
        "UUID": "pydantic.UUID4"
    }
    return translate_dict.get(type_name)


def get_schemas_base_declaration(table: sql_column_parser.schemas.Table):
    declaration = ""
    for column in table.columns:
        if column.is_primary_key and column.col_type.default:
            continue
        line = (
            f"\t{column.name}: {translate_sql_type_to_pytypes(column.col_type.name)}"
        )
        declaration += f"{line}\n"
    return declaration


def get_model_declarations(table: sql_column_parser.schemas.Table):
    declaration = ""
    for column in table.columns:
        line = (f"\t{column.name} = DB.Column(DB."
                f"{translate_sql_type(column.col_type.name)}")
        if column.col_type.max_bytesize:
            line += f"({column.col_type.max_bytesize})"
        else:
            line += "()"
        if column.is_primary_key:
            line += f", primary_key={str(column.is_primary_key)}"
        if column.col_type.default:
            line += f", default=DB.Text(\"{column.col_type.default}\")"
        if not column.col_type.nullable:
            line += f", nullable={column.col_type.nullable}"

        line += ")"
        declaration += f"{line}\n"
    return declaration


def replace_in_file(src_file_path, target_file_path, replacement_dict):
    #input file
    input_file = open(src_file_path, "rt")
    #output file to write the result to
    output_file = open(target_file_path, "wt")
    #for each line in the input file
    for line in input_file:
        for word_to_replace, replacement_word in replacement_dict.items():
            #read replace the string and write to output file
            line = line.replace(word_to_replace, replacement_word)
        output_file.write(line)
    #close input and output files
    input_file.close()
    output_file.close()


def main(sql_file, target_directory, project_name):
    gen_dirs_and_files(sql_file, target_directory, project_name)


def entry_point():
    typer.run(main)
