# explor
Python object explorer which shows you what you can do with an object.

It takes the output from `dir()`, checks this and classifies it in a table.
With that, you don't have to read the entire output of `dir()` and visually
filter it for the relevant information.

## Installation

Install the package:
```bash
pip install explor
```
or
```bash
pip install git+git://github.com/Talon24/explore
```
or
```bash
pip install git+https://github.com/Talon24/explore
```

## Example

From this

```python
# Very long line with very specific information, like all the dunder-methods
import datetime
print(dir(datetime.datetime.now()))
['__add__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__rsub__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', 'astimezone', 'combine', 'ctime', 'date', 'day', 'dst', 'fold', 'fromisocalendar', 'fromisoformat', 'fromordinal', 'fromtimestamp', 'hour', 'isocalendar', 'isoformat', 'isoweekday', 'max', 'microsecond', 'min', 'minute', 'month', 'now', 'replace', 'resolution', 'second', 'strftime', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz', 'today', 'toordinal', 'tzinfo', 'tzname', 'utcfromtimestamp', 'utcnow', 'utcoffset', 'utctimetuple', 'weekday', 'year']
```

To this

```python
from explor import explore as ex
import datetime

ex(datetime.datetime.now())
```
```
  Inherits: 
datetime -> date -> object
╔ Class datetime ══════════════════╦═══════════════════════╦══════╗
║ Methods                          ║ Data                  ║ Ops  ║
╠══════════════════════════════════╬═══════════════════════╬══════╣
║ astimezone      strftime         ║ day: int              ║ !=   ║
║ combine         strptime         ║ fold: int             ║ +    ║
║ ctime           time             ║ hour: int             ║ -    ║
║ date            timestamp        ║ max: datetime         ║ <    ║
║ dst             timetuple        ║ microsecond: int      ║ <=   ║
║ fromisocalendar timetz           ║ min: datetime         ║ ==   ║
║ fromisoformat   today            ║ minute: int           ║ >    ║
║ fromordinal     toordinal        ║ month: int            ║ >=   ║
║ fromtimestamp   tzname           ║ resolution: timedelta ║ hash ║
║ isocalendar     utcfromtimestamp ║ second: int           ║ str  ║
║ isoformat       utcnow           ║ tzinfo: NoneType      ║      ║
║ isoweekday      utcoffset        ║ year: int             ║      ║
║ now             utctimetuple     ║                       ║      ║
║ replace         weekday          ║                       ║      ║
╚══════════════════════════════════╩═══════════════════════╩══════╝
```

## Usage

The module's name is `explore` and it provides a function called `explore()`.
To simplify exploration, I'd recommend aliasing it as something short like `ex`.
### Settings

You can change the style of the table. The `DoubleTable` is the default, if the text viewer can't handle unicode,
then the `AsciiTable` might be useful. Some examples to change the Table style:
```python
import explor
explor.TABLETYPE = explor.terminaltables.AsciiTable
explor.TABLETYPE = explor.terminaltables.SingleTable
explor.TABLETYPE = explor.terminaltables.DoubleTable
explor.TABLETYPE = explor.terminaltables.GithubFlavoredMarkdownTable
```

### Module

```python
from explor import explore as ex
import pathlib

ex(pathlib)
```
```
  Description:
Object-oriented filesystem paths.

This module provides classes to represent abstract paths and concrete
paths with operations that have semantics appropriate for different
operating systems.
╔ module: pathlib ══════╦═════════════════════╦═════════════════╗
║ Constants ║ Modules   ║ Functions           ║ Classes         ║
╠═══════════╬═══════════╬═════════════════════╬═════════════════╣
║ EBADF     ║ fnmatch   ║ urlquote_from_bytes ║ Path            ║
║ ELOOP     ║ functools ║                     ║ PosixPath       ║
║ ENOENT    ║ io        ║                     ║ PurePath        ║
║ ENOTDIR   ║ ntpath    ║                     ║ PurePosixPath   ║
║ S_ISBLK   ║ os        ║                     ║ PureWindowsPath ║
║ S_ISCHR   ║ posixpath ║                     ║ Sequence        ║
║ S_ISDIR   ║ re        ║                     ║ WindowsPath     ║
║ S_ISFIFO  ║ sys       ║                     ║                 ║
║ S_ISLNK   ║ warnings  ║                     ║                 ║
║ S_ISREG   ║           ║                     ║                 ║
║ S_ISSOCK  ║           ║                     ║                 ║
╚═══════════╩═══════════╩═════════════════════╩═════════════════╝
```

### Function

```python
from explor import explore as ex
def a_function(pos: int, /, both: float, untyped=4, *, kw_only: str = "blue") -> complex:
    """Kinds of arguments."""
ex(a_function)
```
```
  Description:
Kinds of arguments.
╔ Function a_function -> complex ════════════════════╗
║ Argument ║ Default ║ Type  ║ Kind                  ║
╠══════════╬═════════╬═══════╬═══════════════════════╣
║ pos      ║ ---     ║ int   ║ positional-only       ║
║ both     ║ ---     ║ float ║ positional or keyword ║
║ untyped  ║ 4       ║ Any   ║ positional or keyword ║
║ kw_only  ║ 'blue'  ║ str   ║ keyword-only          ║
╚══════════╩═════════╩═══════╩═══════════════════════╝
```

### Class

On Classes (Not instances), the constructor is also printed.

```python
from explor import explore as ex
import requests
ex(requests.Request)
```
```
  Inherits: 
Request -> RequestHooksMixin -> object
  Description:
A user-created :class:`Request <Request>` object.
...
╔ type: Request ══╦══════╗
║ Functions       ║ Ops  ║
╠═════════════════╬══════╣
║ deregister_hook ║ !=   ║
║ prepare         ║ <    ║
║ register_hook   ║ <=   ║
║                 ║ ==   ║
║                 ║ >    ║
║                 ║ >=   ║
║                 ║ hash ║
║                 ║ str  ║
╚═════════════════╩══════╝
  Description:
A user-created :class:`Request <Request>` object.
...
╔ Constructor ═══════╗
║ Argument ║ Default ║
╠══════════╬═════════╣
║ method   ║ None    ║
║ url      ║ None    ║
║ headers  ║ None    ║
║ files    ║ None    ║
║ data     ║ None    ║
║ params   ║ None    ║
║ auth     ║ None    ║
║ cookies  ║ None    ║
║ hooks    ║ None    ║
║ json     ║ None    ║
╚══════════╩═════════╝
```

```python
from explor import explore as ex
import fractions
ex(fractions.Fraction)
```
```
  Inherits: 
Fraction -> Rational -> Real -> Complex -> Number -> object
  Description:
This class implements rational numbers.
...
╔ ABCMeta: Fraction ═══════════════╦═══════════════════════╦════════════╗
║ Methods      ║ Functions         ║ Data                  ║ Ops        ║
╠══════════════╬═══════════════════╬═══════════════════════╬════════════╣
║ from_decimal ║ as_integer_ratio  ║ denominator: property ║ !=  ==     ║
║ from_float   ║ conjugate         ║ imag: property        ║ %   >      ║
║              ║ is_integer        ║ numerator: property   ║ *   >=     ║
║              ║ limit_denominator ║ real: property        ║ **  abs    ║
║              ║                   ║                       ║ +   bool   ║
║              ║                   ║                       ║ +() divmod ║
║              ║                   ║                       ║ -   float  ║
║              ║                   ║                       ║ -() hash   ║
║              ║                   ║                       ║ /   int    ║
║              ║                   ║                       ║ //  round  ║
║              ║                   ║                       ║ <   str    ║
║              ║                   ║                       ║ <=         ║
╚══════════════╩═══════════════════╩═══════════════════════╩════════════╝
  Description:
This class implements rational numbers.
...
╔ Constructor ╦═════════╗
║ Argument    ║ Default ║
╠═════════════╬═════════╣
║ numerator   ║ 0       ║
║ denominator ║ None    ║
╚═════════════╩═════════╝
```

## Automatic import
If you have ipython, you can create a file in `~/.ipython/profile_default/startup/` that imports it,
it will then be available at the start of ipython.

This can look like this:
```
from explor import explore as ex
from explor import explore_signature as exs
from explor import explore_object as exo

get_ipython().magic("%autocall 1")  # With this, it's callable without parens; e.g. `ex os.path`
```

More explanation [here](https://towardsdatascience.com/how-to-automatically-import-your-favorite-libraries-into-ipython-or-a-jupyter-notebook-9c69d89aa343).


## Limitations

The library won't always work on some builtin objects like `print` or libraries written in c, e.g. `numpy.array`.
