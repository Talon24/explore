# -*- coding: utf-8 -*-
"""Human readable object exploration module.

It is designed to be more verbose than the dir()-function, while being more
compact than help().
"""

from __future__ import print_function

__author__ = "Talon24"
__license__ = "MIT"
__version__ = "0.1.9"
__maintainer__ = "Talon24"
__url__ = "https://github.com/Talon24/explore"
__status__ = "Developement"

__all__ = ["explore", "explore_object", "explore_signature"]

import pydoc
import inspect
import itertools

import colorama
import terminaltables
# import pkg_resources

colorama.init()

TABLETYPE = terminaltables.DoubleTable
COLORIZE = True

# _MAPPING = pkg_resources.resource_string("explore", "mapping.json")
# Isn't created in a subdirectory without more than one module.
_MAPPING = {
    "__add__": "+",
    "__sub__": "-",
    "__mul__": "*",
    "__truediv__": "/",
    "__floordiv__": "//",
    "__matmul__": "@",
    "__pow__": "**",
    "__mod__": "%",
    "__divmod__": "divmod",
    "__and__": "&",
    "__or__": "|",
    "__xor__": "^",
    "__lshift__": "<<",
    "__rshift__": ">>",
    "__iadd__": "+=",
    "__isub__": "-=",
    "__imul__": "*=",
    "__itruediv__": "/=",
    "__ifloordiv__": "//=",
    "__imatmul__": "@=",
    "__ipow__": "**=",
    "__imod__": "%=",
    "__iand__": "&=",
    "__ior__": "|=",
    "__ixor__": "^=",
    "__ilshift__": "<<=",
    "__irshift__": ">>=",
    "__eq__": "==",
    "__ne__": "!=",
    "__lt__": "<",
    "__gt__": ">",
    "__leq__": "<=",
    "__geq__": ">=",
    "__invert__": "~",
    "__pos__": "+()",
    "__neg__": "-()",
    "__abs__": "abs",
    "__len__": "len",
    "__int__": "int",
    "__float__": "float",
    "__round__": "round",
    "__enter__": "with:",
    "__await__": "await",
    "__contains__": "in",
    "__getitem__": "[]",
    "__setitem__": "[] = x",
    "__delitem__": "del x",
    "__call__": "()"
}


def colored(data, color):
    """Color a string with colorama and reset."""
    if COLORIZE:
        return "{color}{data}{reset}".format(color=color, data=data,
                                             reset=colorama.Style.RESET_ALL)
    else:
        return data


def _map_dunders(thing, items):
    """Match dunder methods to the operator/construct they are related to."""
    ops = []
    for item in items:
        if item in _MAPPING:
            text = _MAPPING[item]
            ops.append(text)
    # Special case: Hash. Classes can have hashes, but not their instances,
    # or hash might be None.
    # list has a __hash__ - attr (None), even though it is not hashable
    if "__hash__" in items and thing.__hash__:
        ops.append("hash")
    return ops


def _prune_data(thing, data):
    """Move items out of the Data row."""
    remappable = ("method_descriptor", "builtin_function_or_method")
    uninteresting = ("PytestTester", "_Feature")
    for item in data["Data"][:]:
        typename = type(getattr(thing, item)).__name__
        if typename in remappable or typename in uninteresting:
            if typename in remappable:
                if inspect.ismodule(thing):
                    data["Functions"].append(item)
                else:
                    data["Methods"].append(item)
            data["Data"].remove(item)


def _prune_arguments_list(data, header):
    """Remove default information from list of arguments if all are unset."""
    type_index = header.index("Type")
    if all(entry[type_index] == "Any" for entry in data):
        for entry in data:
            del entry[type_index]
        del header[type_index]
    kind_index = header.index("Kind")
    if all(entry[kind_index] == "Positional Or Keyword" for entry in data):
        for entry in data:
            del entry[kind_index]
        del header[kind_index]


def explore_signature(thing, show_hidden=False):
    """Show information about a function and its parameters as a table."""
    try:
        signature = inspect.signature(thing)
    except ValueError as exc:
        print(colored("{!r} does not reveal its signature.".format(
            thing), colorama.Fore.RED))
        standard_builtins = (__import__, breakpoint, dir, getattr, iter,
                             max, min, next, print, vars)
        if thing in standard_builtins:
            print(colored("Check the documentation at "
                          "https://docs.python.org/3/library/functions.html#{}"
                          " .".format(thing.__name__), colorama.Fore.RED))
        return
    empty = inspect.Signature.empty
    header = ["Argument", "Default", "Type", "Kind"]
    data = []
    return_type = signature.return_annotation
    for name, parameter in signature.parameters.items():
        # kind = parameter.kind.name.replace("_", " ").title()
        kind = parameter.kind.description
        default = parameter.default
        default = repr(default) if default is not empty else "---"
        annotation = parameter.annotation
        annotation = annotation.__name__ if annotation is not empty else "Any"
        data.append([name, default, annotation, kind])
    # Coloring
    for row in data:
        if row[0] in ("self", "cls"):
            row[0] = colored(row[0], colorama.Fore.YELLOW)
        elif row[1] == "---" and not row[3].startswith("var"):
            # Required argument, as no default is set.
            # Variadic is allowed to be empty, though.
            row[0] = colored(row[0], colorama.Fore.RED)
    if not show_hidden:
        _prune_arguments_list(data, header)
    # Convert to Table
    table = TABLETYPE([header] + data)
    if not inspect.isclass(thing):
        table.title = " Function {} ".format(thing.__name__)
        if return_type is not inspect.Signature.empty:
            table.title += "-> {} ".format(return_type.__name__)
    else:
        table.title = " Constructor "
    description = pydoc.getdoc(thing).split(".")[0]
    if description:
        print("  Description:\n{}.".format(description))
    if not len(data) == 0:
        print(table.table)
    else:
        print("This Function takes no arguments.")


def explore_object(thing, show_hidden=False):
    """Show dir(thing) as a table to make it more human readable."""
    items = set(dir(thing))
    data = dict()
    # Extract members, assign them to categories
    data["Dunders"] = [
        item for item in items if item.startswith("__") and item.endswith("__")]
    items.difference_update(data["Dunders"])
    data["Secrets"] = [
        item for item in items if item.startswith("_")]
    items.difference_update(data["Secrets"])
    data["Constants"] = [
        item for item in items if item.isupper()]
    items.difference_update(data["Constants"])
    data["Modules"] = [
        item for item in items if inspect.ismodule(getattr(thing, item))]
    items.difference_update(data["Modules"])
    data["Methods"] = [
        item for item in items if inspect.ismethod(getattr(thing, item))]
    items.difference_update(data["Methods"])
    data["Functions"] = [
        item for item in items if inspect.isfunction(getattr(thing, item))]
    items.difference_update(data["Functions"])
    data["Classes"] = [
        item for item in items if inspect.isclass(getattr(thing, item))]
    items.difference_update(data["Classes"])
    data["Data"] = list(items)
    data["Ops"] = _map_dunders(thing, data["Dunders"])
    _prune_data(thing, data)

    # color operators
    data["Ops"] = [colored(text, colorama.Fore.LIGHTBLUE_EX)
                   for text in data["Ops"]
                   if text.isalpha()]

    if not show_hidden:
        hidden_names = ["Secrets", "Dunders"]
        for name in hidden_names:
            try:
                del data[name]
            except KeyError:
                pass
    # color types
    newdata = []
    for item in data["Data"]:
        type_ = colored(type(getattr(thing, item)).__name__,
                        colorama.Fore.LIGHTCYAN_EX)
        newdata.append("{}: {}".format(item, type_))
    data["Data"] = newdata

    # list-of-colums to list-of-rows
    with_header = [
        [key] + sorted(value) for key, value in data.items() if len(value) > 0]
    rotated = [row for row in itertools.zip_longest(*with_header, fillvalue="")]
    table = TABLETYPE(rotated)
    try:
        table.title = " {}: {} ".format(type(thing).__name__, thing.__name__)
    except AttributeError:
        table.title = " Class {} ".format(type(thing).__name__)
    descr = pydoc.getdoc(thing).split(".")[0]
    if descr:
        print("  Description:\n{}.".format(descr))
    print(table.table)


def explore(thing, show_hidden=False):
    """Show what you can do with an object.

    Depending on the with explore_function or explore_object.
    Note that built-in objects or functions might not be matched correctly.
    """
    if (
            inspect.isfunction(thing) or
            inspect.ismethod(thing) or
            inspect.isbuiltin(thing)  # This can miss, e.g. print, namedtuple
    ):
        explore_signature(thing, show_hidden=show_hidden)
    elif inspect.isclass(thing):
        explore_object(thing, show_hidden=show_hidden)
        explore_signature(thing, show_hidden=show_hidden)
    else:
        explore_object(thing, show_hidden=show_hidden)


if __name__ == '__main__':
    # explore(1)
    # explore("")
    # explore(list)
    # explore(complex)
    # def a_function(pos: int, /, both: float, untyped=4, *, kw_only: str = "blue") -> complex:
    #     """Kinds of arguments."""
    # def variadic_function(*args, reverse=True, **kwargs):
    #     """Variadic arguments."""
    # explore(a_function)
    # explore(variadic_function)
    # import requests
    # explore(requests.Request)
    import datetime
    explore(datetime.datetime.now())
    # import pathlib
    # explore(pathlib)
    import fractions
    explore(fractions.Fraction)
    # explore(open)
    explore(property)
