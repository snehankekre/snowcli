#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.dir_util import copy_tree
import os
from pathlib import Path
import pkg_resources
import typer

from snowcli.cli.snowpark_shared import snowpark_create, snowpark_update, snowpark_package, snowpark_execute, snowpark_describe, snowpark_list, snowpark_drop
from snowcli.utils import conf_callback

app = typer.Typer()
EnvironmentOption = typer.Option("dev", help='Environment name', callback=conf_callback, is_eager=True)

@app.command("init")
def procedure_init():
    """
    Initialize this directory with a sample set of files to create a procedure.
    """
    copy_tree(pkg_resources.resource_filename(
        'templates', 'default_procedure'), f'{os.getcwd()}')

@app.command("create")
def procedure_create(environment: str = EnvironmentOption,
                    name: str = typer.Option(..., '--name', '-n',
                                             help="Name of the procedure"),
                    file: Path = typer.Option('app.zip',
                                              '--file',
                                              '-f', 
                                              help='Path to the file or folder to deploy',
                                              exists=True,
                                              readable=True,
                                              file_okay=True),
                    handler: str = typer.Option(...,
                                                '--handler',
                                                '-h',
                                                help='Handler'),
                    input_parameters: str = typer.Option(...,
                                                         '--input-parameters',
                                                         '-i',
                                                         help='Input parameters - such as (message string, count int)'),
                    return_type: str = typer.Option(...,
                                                    '--return-type',
                                                    '-r',
                                                    help='Return type'),
                    overwrite: bool = typer.Option(False,
                                                   '--overwrite',
                                                   '-o',
                                                   help='Replace if existing procedure'),
                    execute_as_caller: bool = typer.Option(False, '--execute-as-caller', help='Execute as caller')
                    ):
    snowpark_package()
    snowpark_create('procedure', environment, name, file, handler, input_parameters, return_type, overwrite, execute_as_caller)

@app.command("update")
def procedure_update(environment: str = EnvironmentOption,
                    name: str = typer.Option(..., '--name', '-n', help="Name of the procedure"),
                    file: Path = typer.Option('app.zip',
                                              '--file',
                                              '-f', 
                                              help='Path to the file to update',
                                              exists=True,
                                              readable=True,
                                              file_okay=True),
                    handler: str = typer.Option(...,
                                                '--handler',
                                                '-h',
                                                help='Handler'),
                    input_parameters: str = typer.Option(...,
                                                         '--input-parameters',
                                                         '-i',
                                                         help='Input parameters - such as (message string, count int)'),
                    return_type: str = typer.Option(...,
                                                    '--return-type',
                                                    '-r',
                                                    help='Return type'),
                    replace: bool = typer.Option(False, 
                                                '--replace-always', '-r', 
                                                help='Replace procedure, even if no detected changes to metadata'),
                    execute_as_caller: bool = typer.Option(False, '--execute-as-caller', help='Execute as caller')):
    snowpark_package()
    snowpark_update('procedure', environment, name, file, handler, input_parameters, return_type, replace, execute_as_caller)

@app.command("package")
def procedure_package():
    snowpark_package()

@app.command("execute")
def procedure_execute(environment: str = EnvironmentOption,
                     select: str = typer.Option(..., '--procedure', '-p', help='Procedure with inputs. E.g. \'hello(int, string)\'')):
    snowpark_execute('procedure', environment, select)


@app.command("describe")
def procedure_describe(environment: str = EnvironmentOption,
                      name: str = typer.Option('', '--name', '-n', help="Name of the procedure"),
                      input_parameters: str = typer.Option('',
                                                         '--input-parameters',
                                                         '-i',
                                                         help='Input parameters - such as (message string, count int)'),
                      signature: str = typer.Option('', '--procedure', '-p', help='Procedure signature with inputs. E.g. \'hello(int, string)\'')
                      ):
    snowpark_describe('procedure', environment, name, input_parameters, signature)

@app.command("list")
def procedure_list(environment: str = EnvironmentOption,
                   like: str = typer.Option('%%', '--like', '-l', help='Filter procedures by name - e.g. "hello%"')):
    snowpark_list('procedure', environment, like=like)

@app.command("drop")
def procedure_drop(environment: str = EnvironmentOption,
                      name: str = typer.Option('', '--name', '-n', help="Name of the procedure"),
                      input_parameters: str = typer.Option('',
                                                         '--input-parameters',
                                                         '-i',
                                                         help='Input parameters - such as (message string, count int)'),
                      signature: str = typer.Option('', '--procedure', '-p', help='Procedure signature with inputs. E.g. \'hello(int, string)\'')
                      ):
    snowpark_drop('procedure', environment, name, input_parameters, signature)