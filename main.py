import os

from django.utils.module_loading import import_string
from exceptions import (PathDoesNotExists, ScriptContextDoesNotExists,
                        MethodNameRequired, MethodNotFound, MethodTypeError,
                        KlassImportError)
from models import db, Script


def is_script_file_exists(path=None):
    if not path:
        raise PathDoesNotExists
    return True if os.path.isfile(path) else False


def create_script(path=None, context=None):
    if not path:
        raise PathDoesNotExists
    if not context:
        raise ScriptContextDoesNotExists

    with open(path, 'w') as file:
        file.write(context)


def remove_script(path=None):
    if not path:
        raise PathDoesNotExists
    os.remove(path)


def executor(script, method_kwargs_data=None, use_dynamic=True,
             klass_kwargs_data=None):
    dotted_path = script.importable_path
    if not klass_kwargs_data:
        klass_kwargs_data = script.initialization_params

    method_requirements = script.method_requirements

    method_name = method_requirements.get('method_name')
    if not method_name and use_dynamic:
        raise MethodNameRequired

    method_kwargs = method_requirements.get('kwargs')
    if not method_kwargs_data:
        method_kwargs_data = {}

    try:
        klass = import_string(dotted_path=dotted_path)(**klass_kwargs_data)
        if not use_dynamic:
            return klass
        klass_func = getattr(klass, method_name)
        if callable(klass_func):
            return klass_func(**method_kwargs_data)
        else:
            raise MethodNotFound
    except TypeError as e:
        message = f"Type Error: {e}\n" \
                  f"Method Name: {method_name}\n" \
                  f"Method Kwargs: {method_kwargs}"
        raise MethodTypeError(message=message)
    except ImportError as e:
        message = f"{e}\n" \
                  f"Import path: {dotted_path}\n" \
                  f"{script.script}"
        raise KlassImportError(message=message)


def main(script=None, method_kwargs_data=None, use_dynamic=True,
         klass_kwargs_data=None):
    if not script:
        return

    if is_script_file_exists(path=script.path):
        remove_script(path=script.path)

    create_script(path=script.path, context=script.script)

    result = executor(script=script, method_kwargs_data=method_kwargs_data,
                      use_dynamic=use_dynamic,
                      klass_kwargs_data=klass_kwargs_data)

    remove_script(path=script.path)

    return result


if db.is_closed():
    db.connect()
db.create_tables([Script])
