import re
import sys
import unittest

import io
import contextlib

import explor
explor.COLORIZE = False


class MyTestCase(unittest.TestCase):
    """Generate examples with
    explor.COLORIZE = False
    stringio = io.StringIO()
    with pycopy(output).redirect_stdout(stringio):
        explor.explore(...)
    output = stringio.getvalue()
    pypaste(output)
    """

    def test_correct_version(self):
        """Check that the version of python matches so that the builtin api is as expected."""
        version = sys.version_info
        self.assertEqual(version.major, 3)
        self.assertEqual(version.minor, 12)

    def test_string(self):
        self.maxDiff = None
        stringio = io.StringIO()
        with contextlib.redirect_stdout(stringio):
            explor.explore(str)
        output = stringio.getvalue()
        raw = """  Description:
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str
...
╔ type: str ═════════════════════════╦══════╗
║ Methods                            ║ Ops  ║
╠════════════════════════════════════╬══════╣
║ capitalize isidentifier rfind      ║ !=   ║
║ casefold   islower      rindex     ║ %    ║
║ center     isnumeric    rjust      ║ *    ║
║ count      isprintable  rpartition ║ +    ║
║ encode     isspace      rsplit     ║ <    ║
║ endswith   istitle      rstrip     ║ <=   ║
║ expandtabs isupper      split      ║ ==   ║
║ find       join         splitlines ║ >    ║
║ format     ljust        startswith ║ >=   ║
║ format_map lower        strip      ║ []   ║
║ index      lstrip       swapcase   ║ for: ║
║ isalnum    maketrans    title      ║ hash ║
║ isalpha    partition    translate  ║ in   ║
║ isascii    removeprefix upper      ║ len  ║
║ isdecimal  removesuffix zfill      ║ str  ║
║ isdigit    replace                 ║      ║
╚════════════════════════════════════╩══════╝
<class 'str'> does not reveal its signature.
"""
        self.assertEqual(output, raw)

    def test_int(self):
        self.maxDiff = None
        stringio = io.StringIO()
        with contextlib.redirect_stdout(stringio):
            explor.explore(int)
        output = stringio.getvalue()
        raw = """  Description:
int([x]) -> integer
int(x, base=10) -> integer
...
╔ type: int ═══════╦════════════════════════════════╦════════════╗
║ Methods          ║ Data                           ║ Ops        ║
╠══════════════════╬════════════════════════════════╬════════════╣
║ as_integer_ratio ║ denominator: getset_descriptor ║ !=  >      ║
║ bit_count        ║ imag: getset_descriptor        ║ %   >=     ║
║ bit_length       ║ numerator: getset_descriptor   ║ &   >>     ║
║ conjugate        ║ real: getset_descriptor        ║ *   ^      ║
║ from_bytes       ║                                ║ **  abs    ║
║ is_integer       ║                                ║ +   bool   ║
║ to_bytes         ║                                ║ +() divmod ║
║                  ║                                ║ -   float  ║
║                  ║                                ║ -() hash   ║
║                  ║                                ║ /   int    ║
║                  ║                                ║ //  round  ║
║                  ║                                ║ <   str    ║
║                  ║                                ║ <<  |      ║
║                  ║                                ║ <=  ~      ║
║                  ║                                ║ ==         ║
╚══════════════════╩════════════════════════════════╩════════════╝
<class 'int'> does not reveal its signature.
"""
        self.assertEqual(output, raw)

    def test_list(self):
        # raw will be pasted in later
        self.maxDiff = None
        stringio = io.StringIO()
        with contextlib.redirect_stdout(stringio):
            explor.explore(list)
        output = stringio.getvalue()
        raw = """  Description:
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
╔ type: list ═════════╗
║ Methods ║ Ops       ║
╠═════════╬═══════════╣
║ append  ║ != >=     ║
║ clear   ║ *  []     ║
║ copy    ║ *= [] = x ║
║ count   ║ +  del x  ║
║ extend  ║ += for:   ║
║ index   ║ <  in     ║
║ insert  ║ <= len    ║
║ pop     ║ == str    ║
║ remove  ║ >         ║
║ reverse ║           ║
║ sort    ║           ║
╚═════════╩═══════════╝
  Description:
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
╔ Constructor ═══════╦═════════════════╗
║ Argument ║ Default ║ Kind            ║
╠══════════╬═════════╬═════════════════╣
║ iterable ║ ()      ║ positional-only ║
╚══════════╩═════════╩═════════════════╝
"""
        self.assertEqual(output, raw)

    def test_module(self):
        self.maxDiff = None
        stringio = io.StringIO()
        with contextlib.redirect_stdout(stringio):
            explor.explore(re)
        output = stringio.getvalue()
        raw = """  Description:
Support for regular expressions (RE).
...
╔ module: re ══════════╦═══════════╦═══════════╦═══════════╗
║ Constants            ║ Modules   ║ Functions ║ Classes   ║
╠══════════════════════╬═══════════╬═══════════╬═══════════╣
║ A          MULTILINE ║ copyreg   ║ compile   ║ Match     ║
║ ASCII      NOFLAG    ║ enum      ║ escape    ║ Pattern   ║
║ DEBUG      S         ║ functools ║ findall   ║ RegexFlag ║
║ DOTALL     T         ║           ║ finditer  ║ Scanner   ║
║ I          TEMPLATE  ║           ║ fullmatch ║ error     ║
║ IGNORECASE U         ║           ║ match     ║           ║
║ L          UNICODE   ║           ║ purge     ║           ║
║ LOCALE     VERBOSE   ║           ║ search    ║           ║
║ M          X         ║           ║ split     ║           ║
║                      ║           ║ sub       ║           ║
║                      ║           ║ subn      ║           ║
║                      ║           ║ template  ║           ║
╚══════════════════════╩═══════════╩═══════════╩═══════════╝
"""
        self.assertEqual(output, raw)

    def test_signature(self):
        self.maxDiff = None
        stringio = io.StringIO()
        def a_function(pos: int, /, both: float, untyped=4, *, kw_only: str = "blue") -> complex:
            """Kinds of arguments."""
        with contextlib.redirect_stdout(stringio):
            explor.explore(a_function)
        output = stringio.getvalue()
        raw = '''  Description:
Kinds of arguments.
╔ Function a_function -> complex ════════════════════╗
║ Argument ║ Default ║ Type  ║ Kind                  ║
╠══════════╬═════════╬═══════╬═══════════════════════╣
║ pos      ║ ---     ║ int   ║ positional-only       ║
║ both     ║ ---     ║ float ║ positional or keyword ║
║ untyped  ║ 4       ║ Any   ║ positional or keyword ║
║ kw_only  ║ 'blue'  ║ str   ║ keyword-only          ║
╚══════════╩═════════╩═══════╩═══════════════════════╝
'''
        self.assertEqual(output, raw)


if __name__ == '__main__':
    unittest.main()
