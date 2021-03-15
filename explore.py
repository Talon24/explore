"""Pretty-print dir() result."""

import json
import inspect

import six
import colorama
import terminaltables

colorama.init()


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


def _map_dunders(thing, items):
    """Process the Dunder methods to make them more human readable."""
    ops = []
    for item in items:
        if item in _MAPPING:
            text = _MAPPING[item]
            if not text.isalpha():
                text = "{}{}{}".format(colorama.Fore.LIGHTBLUE_EX, text, colorama.Fore.RESET)
            ops.append(text)
    # Special case: Hash. Classes can have hashes, but not their instances, or hash might be None.
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


def explore(thing, show_hidden=False):
    """Show dir(thing) as a table, sorting its members to make it more human readable."""
    items = set(dir(thing))
    data = dict()
    data["Dunders"] = [item for item in items if item.startswith("__") and item.endswith("__")]
    items.difference_update(data["Dunders"])
    data["Secrets"] = [item for item in items if item.startswith("_")]
    items.difference_update(data["Secrets"])
    data["Constants"] = [item for item in items if item.isupper()]
    items.difference_update(data["Constants"])
    data["Modules"] = [item for item in items if inspect.ismodule(getattr(thing, item))]
    items.difference_update(data["Modules"])
    data["Methods"] = [item for item in items if inspect.ismethod(getattr(thing, item))]
    items.difference_update(data["Methods"])
    data["Functions"] = [item for item in items if inspect.isfunction(getattr(thing, item))]
    items.difference_update(data["Functions"])
    data["Classes"] = [item for item in items if inspect.isclass(getattr(thing, item))]
    items.difference_update(data["Classes"])
    data["Data"] = list(items)
    data["Ops"] = _map_dunders(thing, data["Dunders"])

    _prune_data(thing, data)
    data_pattern = "{{}}: {}{{}}{}".format(colorama.Fore.LIGHTCYAN_EX, colorama.Fore.RESET)
    data["Data"] = [data_pattern.format(item, type(getattr(thing, item)).__name__) for item in data["Data"]]

    if not show_hidden:
        hidden_names = ["Secrets", "Dunders"]
        for name in hidden_names:
            try:
                del data[name]
            except KeyError:
                pass
    data2 = [[key] + sorted(value) for key, value in data.items() if len(value) > 0]
    rotated = [row for row in six.moves.zip_longest(*data2, fillvalue="")]
    table = terminaltables.DoubleTable(rotated)
    try:
        table.title = " {}: {} ".format(type(thing).__name__, thing.__name__)
    except AttributeError:
        table.title = " Class {} ".format(type(thing).__name__)
    print(table.table)


if __name__ == '__main__':
    explore(1)
    explore("")
    explore(list)
    explore(set)
