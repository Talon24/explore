# -*- coding: utf-8 -*-
"""Human-readable object exploration module.

It is designed to be more verbose than the dir()-function, while being more
compact than help().
"""

from __future__ import print_function

# pylint: disable=no-else-return
# pylint: disable=consider-using-f-string

__author__ = "Talon24"
__license__ = "MIT"
__version__ = "0.1.21"
__maintainer__ = "Talon24"
__url__ = "https://github.com/Talon24/explore"
__status__ = "Development"

__all__ = ["explore", "explore_object", "explore_signature"]

import copy
import pydoc
import shutil
import typing
import inspect
import itertools
import collections

import colorama
import terminaltables

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
    "__le__": "<=",
    "__ge__": ">=",
    "__invert__": "~",
    "__pos__": "+()",
    "__neg__": "-()",
    "__abs__": "abs",
    "__len__": "len",
    "__int__": "int",
    "__str__": "str",
    "__bool__": "bool",
    "__float__": "float",
    "__bytes__": "bytes",
    "__round__": "round",
    "__await__": "await",
    "__enter__": "with:",
    "__iter__": "for:",
    "__contains__": "in",
    "__getitem__": "[]",
    "__setitem__": "[] = x",
    "__delitem__": "del x",
    "__call__": "()",
}


class ObjectProperties:
    """Class to store the properties of an object."""

    def __init__(self, thing):
        items = set(dir(thing))

        # Check for __all__ members that are not in dir()
        if inspect.ismodule(thing) and hasattr(thing, "__all__"):
            extras = set(thing.__all__).difference(items)
            self.extras_all = sorted(extras)
        else:
            self.extras_all = []
        # Check if item is reachable
        for item in sorted(items):
            try:
                getattr(thing, item)
            except Exception as ex:  # pylint: disable=broad-except
                items.remove(item)
                print(colored("Couldn't access property {} of {!r} because {}".format(item, thing, ex),
                              colorama.Fore.LIGHTRED_EX))
        items = _apply_custom_filters(items, thing)

        self.thing = thing
        self.dunders = sorted([item for item in items if item.startswith("__") and item.endswith("__")])
        items.difference_update(self.dunders)
        self.secrets = sorted([item for item in items if item.startswith("_")])
        items.difference_update(self.secrets)
        self.constants = sorted([item for item in items if item.isupper()])
        items.difference_update(self.constants)
        self.modules = sorted([item for item in items if inspect.ismodule(getattr(thing, item))])
        items.difference_update(self.modules)
        self.methods = sorted([item for item in items if inspect.ismethod(getattr(thing, item))])
        items.difference_update(self.methods)
        self.functions = sorted([
            item for item in items
            if (inspect.isfunction(getattr(thing, item))
                or type(getattr(thing, item)).__name__ == "cython_function_or_method")])
        items.difference_update(self.functions)
        self.classes = sorted([item for item in items if inspect.isclass(getattr(thing, item))])
        items.difference_update(self.classes)
        self.data = list(items)
        self.prune_data()
        self.ops = sorted(self._map_dunders(thing, self.dunders))
        self.parents = self.parent_order(thing)
        self.description = docstring_head(thing)

    def prune_data(self):
        """Move items out of the Data row."""
        remappable = ("method_descriptor", "builtin_function_or_method")
        uninteresting = ("PytestTester", "_Feature")
        for item in self.data[:]:
            typename = type(getattr(self.thing, item)).__name__
            if typename in remappable or typename in uninteresting:
                if typename in remappable:
                    if inspect.ismodule(self.thing):
                        self.functions.append(item)
                    else:
                        self.methods.append(item)
                self.data.remove(item)
        self.data.sort()
        self.functions.sort()
        self.methods.sort()

    def color_operators(self):
        self.ops = [colored(text, colorama.Fore.LIGHTGREEN_EX) for text in self.ops]

    @staticmethod
    def _map_dunders(thing, items):
        """Match dunder methods to the operator/construct they are related to."""
        ops = []
        for item in items[:]:
            if item in _MAPPING:
                text = _MAPPING[item]
                items.remove(item)
                ops.append(text)
        # Special case: Hash. Classes can have hashes, but not their instances,
        # or hash might be None.
        # list has a __hash__ - attr (None), even though it is not hashable
        if "__hash__" in items and thing.__hash__:
            ops.append("hash")
        return ops

    @staticmethod
    def parent_order(thing):
        """Generate a string of parents of the given object."""
        try:
            parents = inspect.getmro(thing)
        except AttributeError:
            parents = inspect.getmro(thing.__class__)
        if not parents:
            # If the object interferes with __mro__, try to get the parents from the class instead.
            parents = inspect.getmro(thing.__class__)
        if not parents[1:] == (object,) and hasattr(parents, "__iter__"):
            return " -> ".join(parent.__name__ for parent in parents)
        return None

    @property
    def dict(self):
        """Return the propertiRes as a dictionary."""
        return {
            "Dunders": self.dunders,
            "Secrets": self.secrets,
            "Constants": self.constants,
            "Modules": self.modules,
            "Methods": self.methods,
            "Functions": self.functions,
            "Classes": self.classes,
            "Data": self.data,
            "Ops": self.ops,
            "Extras": self.extras_all,
        }

    def color_types(self):
        """Color the types for better readability."""
        self.data = [
            "{}: {}".format(item, colored(type(getattr(self.thing, item)).__name__, colorama.Fore.LIGHTCYAN_EX))
            for item in self.data]


class SignatureProperties:
    """Class to store the properties of a function signature."""

    def __init__(self, thing, show_hidden: bool):
        self.thing = thing
        self.error = None
        try:
            self.signature = inspect.signature(thing)
        except ValueError:
            self.error = colored("{!r} does not reveal its signature.".format(thing), colorama.Fore.RED)
            try:
                standard_builtins = (__import__, breakpoint, dir, getattr, iter,
                                     max, min, next, print, vars)
            except NameError:  # 3.5 doesn't know breakpoint
                standard_builtins = (__import__, dir, getattr, iter,
                                     max, min, next, print, vars)
            if thing in standard_builtins:
                self.error += "\n" + colored("Check the documentation at "
                                             "https://docs.python.org/3/library/functions.html#{}"
                                             " .".format(thing.__name__), colorama.Fore.RED)
            return
        self.parameters = self.signature.parameters
        self.return_type = self.signature.return_annotation
        self.header = ["Argument", "Default", "Type", "Kind"]
        self.data = []
        self._extract_arguments(show_hidden)

    def _extract_arguments(self, show_hidden):
        """Extract the arguments from the signature."""
        for name, parameter in self.parameters.items():
            kind = parameter.kind.description
            default = parameter.default
            default = repr(default) if default is not inspect.Signature.empty else "---"
            annotation = self._simplify_annotation(parameter.annotation, show_hidden)
            self.data.append([name, default, annotation, kind])

    def prune_arguments(self):
        """Remove default information from list of arguments if all are unset."""
        type_index = self.header.index("Type")
        if all(entry[type_index] == "Any" for entry in self.data):
            for entry in self.data:
                del entry[type_index]
            del self.header[type_index]
        kind_index = self.header.index("Kind")
        if all(entry[kind_index].lower() == "Positional Or Keyword".lower() for entry in self.data):
            for entry in self.data:
                del entry[kind_index]
            del self.header[kind_index]

    @property
    def dict(self):
        """Return the properties as a dictionary."""
        return {
            "Header": self.header,
            "Data": self.data,
            "ReturnType": self.return_type,
        }

    @staticmethod
    def _simplify_annotation(annotation, show_hidden):
        """Make the annotation more human-readable."""
        if annotation is inspect.Signature.empty:
            annotation = "Any"
        elif typing.get_origin(annotation) is typing.Annotated:  # pylint: disable=protected-access
            # raise ValueError("Annotated type found!!!!!.")
            origin = typing._type_repr(annotation.__origin__)  # pylint: disable=protected-access
            annotation = "[{}] {}".format(
                origin if show_hidden else origin.split(".")[-1],
                ", ".join(repr(a) for a in annotation.__metadata__))
        elif isinstance(annotation, str):
            pass
        elif hasattr(annotation, "__args__"):
            # Type has arguments like list[int]
            pass
        else:
            annotation = annotation.__name__
        return annotation

    def colorize_data(self):
        """Color the data for better readability."""
        for row in self.data:
            if row[0] in ("self", "cls"):
                row[0] = colored(row[0], colorama.Fore.YELLOW)
            elif row[1] == "---" and not row[3].startswith("var"):
                # Required argument, as no default is set.
                # Variadic is allowed to be empty, though.
                row[0] = colored(row[0], colorama.Fore.RED)


def _print_signature_result(thing, data, return_type, table):
    """Write the analysis result back."""
    if not inspect.isclass(thing):
        table.title = " Function {} ".format(thing.__name__)
        if isinstance(return_type, str):
            table.title += "-> {} ".format(return_type)
        elif return_type is not inspect.Signature.empty:
            table.title += "-> {} ".format(return_type.__name__)
    else:
        table.title = " Constructor "
    description = docstring_head(thing)
    if description:
        print("  Description:\n{}".format(description))
    if data:
        print(table.table)
    else:
        print("This Function takes no arguments.")


def _make_table(data, thing):
    """Convert list-of-columns to list-of-rows."""
    with_header = [
        [key] + value for key, value in data.items() if len(value) > 0]
    rotated = list(itertools.zip_longest(*with_header, fillvalue=""))
    table = TABLETYPE(rotated)
    _set_table_title(thing, table)
    return table


def _fold_list(data, columns):
    """Convert one column of data to <columns> columns, aligned."""
    rows, remainder = divmod(len(data), columns)
    chunked = (data[col * rows + min(col, remainder):(col + 1) * rows + min(col + 1, remainder)]
               for col in range(columns))
    folded = [["{item:{length}}".format(item=cell, length=max(len(cell_) for cell_ in col))
               for cell in col]
              for col in chunked]
    block = [" ".join(items) for items in itertools.zip_longest(*folded, fillvalue="")]
    return block


def _minify_data(source_data, thing):
    """Compress too long lists."""
    term_size = shutil.get_terminal_size((80, 20))
    data = copy.deepcopy(source_data)
    # The candidate is the longest column
    candidate_key, candidate_list = max(data.items(), key=lambda x: len(x[1]))
    table = _make_table(data, thing)
    foldings = collections.defaultdict(lambda: 1)
    buffer = 4  # The table has 4 additional lines
    # In every iteration, fold the currently longest column
    # until the table is small enough or too wide.
    while table.table_width < term_size.columns and len(candidate_list) + buffer > term_size.lines:
        foldings[candidate_key] += 1
        new = _fold_list(source_data[candidate_key], foldings[candidate_key])
        data_candidate = copy.deepcopy(data)
        data_candidate[candidate_key] = new
        table = _make_table(data_candidate, thing)
        if len(candidate_list) + buffer < term_size.lines or table.table_width > term_size.columns:
            break
        data = data_candidate
        candidate_key, candidate_list = max(data.items(), key=lambda x: len(x[1]))
    return data


def _set_table_title(thing, table):
    """Infer the title of the table from the object type."""
    try:
        table.title = " {}: {} ".format(type(thing).__name__, thing.__name__)
    except AttributeError:
        table.title = " Class {} ".format(type(thing).__name__)


def _apply_custom_filters(items, thing):
    """Ignore some of the fields if they don't provide good information."""
    # PrefixUnits spam the table, as they show the same base units 20 times
    items = (item for item in items
             if not (type(thing).__name__ == "module"
                     and thing.__name__ == "astropy.units"
                     and type(getattr(thing, item)).__name__ == "PrefixUnit"))
    return set(items)


def colored(data: str, color: str) -> str:
    """Color a string with colorama and reset if allowed to do so."""
    if COLORIZE:
        return "{color}{data}{reset}".format(color=color, data=data,
                                             reset=colorama.Style.RESET_ALL)
    else:
        return data


def docstring_head(thing):
    """Extract the head of a doc string."""
    doc = pydoc.getdoc(thing)
    if len(doc.splitlines()) < 10:
        # docstring is short enough
        return doc
    else:
        first_par = doc.partition("\n\n")[0]
        if len(first_par.splitlines()) < 10:
            # docstring has a paragraph that is short enough
            return first_par + "\n..."
        else:
            # only head of docstring
            return "\n".join(doc.splitlines()[:10]) + "\n..."


def explore_signature(thing: object, show_hidden: bool = False):
    """Show information about a function and its parameters as a table."""
    properties = SignatureProperties(thing, show_hidden)
    if properties.error:
        print(properties.error)
        return
    if not show_hidden:
        properties.prune_arguments()
    # Convert to Table

    table = TABLETYPE([properties.header] + properties.data)
    _print_signature_result(thing, properties.dict, properties.return_type, table)


def explore_object(thing, show_hidden=False, folding=True):
    """Show dir(thing) as a table to make it more human-readable."""
    # data = _extract_members(thing)
    properties = ObjectProperties(thing)

    # color operators
    properties.color_operators()

    if not show_hidden:
        properties.secrets = []
        properties.dunders = []
    properties.color_types()
    if folding:
        minified_data = _minify_data(properties.dict, thing)
    else:
        minified_data = properties.dict

    if properties.parents:
        print("  Inherits: \n{}".format(properties.parents))
    if properties.description:
        print("  Description:\n{}".format(properties.description))
    table = _make_table(minified_data, thing)
    print(table.table)


def explore(thing, show_hidden=False, folding=True):
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
        explore_object(thing, show_hidden=show_hidden, folding=folding)
        explore_signature(thing, show_hidden=show_hidden)
    else:
        explore_object(thing, show_hidden=show_hidden, folding=folding)


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
