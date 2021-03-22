# explore
Python object explorer which shows you what you can do with an object.

It takes the output from `dir()`, checks this and classifies it in a table.
With that, you don't have to read the entire output of `dir()` and visually
filter it for the relevant information.

## Installation

Install the package:
```bash
pip install object-explore
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
['__add__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__rsub__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', 'astimezone', 'combine', 'ctime', 'date', 'day', 'dst', 'fold', 'fromisocalendar', 'fromisoformat', 'fromordinal', 'fromtimestamp', 'hour', 'isocalendar', 'isoformat', 'isoweekday', 'max', 'microsecond', 'min', 'minute', 'month', 'now', 'replace', 'resolution', 'second', 'strftime', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz', 'today', 'toordinal', 'tzinfo', 'tzname', 'utcfromtimestamp', 'utcnow', 'utcoffset', 'utctimetuple', 'weekday', 'year']
```

To this

```python
from explore import explore as ex
import datetime

ex(datetime.datetime.now())
```
```
  Description:
datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required.
╔Class datetime════╦═══════════════════════╦══════╗
║ Methods          ║ Data                  ║ Ops  ║
╠══════════════════╬═══════════════════════╬══════╣
║ astimezone       ║ day: int              ║ !=   ║
║ combine          ║ fold: int             ║ +    ║
║ ctime            ║ hour: int             ║ -    ║
║ date             ║ max: datetime         ║ <    ║
║ dst              ║ microsecond: int      ║ ==   ║
║ fromisocalendar  ║ min: datetime         ║ >    ║
║ fromisoformat    ║ minute: int           ║ hash ║
║ fromordinal      ║ month: int            ║      ║
║ fromtimestamp    ║ resolution: timedelta ║      ║
║ isocalendar      ║ second: int           ║      ║
║ isoformat        ║ tzinfo: NoneType      ║      ║
║ isoweekday       ║ year: int             ║      ║
║ now              ║                       ║      ║
║ replace          ║                       ║      ║
║ strftime         ║                       ║      ║
║ strptime         ║                       ║      ║
║ time             ║                       ║      ║
║ timestamp        ║                       ║      ║
║ timetuple        ║                       ║      ║
║ timetz           ║                       ║      ║
║ today            ║                       ║      ║
║ toordinal        ║                       ║      ║
║ tzname           ║                       ║      ║
║ utcfromtimestamp ║                       ║      ║
║ utcnow           ║                       ║      ║
║ utcoffset        ║                       ║      ║
║ utctimetuple     ║                       ║      ║
║ weekday          ║                       ║      ║
╚══════════════════╩═══════════════════════╩══════╝
```

## Usage

The module's name is `explore` and it provides a function called `explore()`.
To simplify exploration, i'd recommend aliasing it as something short like `ex`. 
### Settings

You can change the style of the table. The `SingleTable` is the default, if the text viewer can't handle unicode,
then the `AsciiTable` might be useful.
```python
import explore
explore.TABLETYPE = explore.terminaltables.AsciiTable
explore.TABLETYPE = explore.terminaltables.SingleTable
explore.TABLETYPE = explore.terminaltables.DoubleTable
explore.TABLETYPE = explore.terminaltables.GithubFlavoredMarkdownTable
```

### Module

```python
from explore import explore as ex
import pathlib

ex(pathlib)
```
```
╔module: pathlib════════╦═════════════════════╦═════════════════╦═════════════════════════╗
║ Constants ║ Modules   ║ Functions           ║ Classes         ║ Data                    ║
╠═══════════╬═══════════╬═════════════════════╬═════════════════╬═════════════════════════╣
║ EBADF     ║ fnmatch   ║ urlquote_from_bytes ║ Path            ║ supports_symlinks: bool ║
║ EINVAL    ║ functools ║                     ║ PosixPath       ║                         ║
║ ELOOP     ║ io        ║                     ║ PurePath        ║                         ║
║ ENOENT    ║ nt        ║                     ║ PurePosixPath   ║                         ║
║ ENOTDIR   ║ ntpath    ║                     ║ PureWindowsPath ║                         ║
║ S_ISBLK   ║ os        ║                     ║ Sequence        ║                         ║
║ S_ISCHR   ║ posixpath ║                     ║ WindowsPath     ║                         ║
║ S_ISDIR   ║ re        ║                     ║ attrgetter      ║                         ║
║ S_ISFIFO  ║ sys       ║                     ║                 ║                         ║
║ S_ISLNK   ║           ║                     ║                 ║                         ║
║ S_ISREG   ║           ║                     ║                 ║                         ║
║ S_ISSOCK  ║           ║                     ║                 ║                         ║
╚═══════════╩═══════════╩═════════════════════╩═════════════════╩═════════════════════════╝
```

### Function

```python
from explore import explore as ex
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
║ pos      ║ ---     ║ int   ║ Positional Only       ║
║ both     ║ ---     ║ float ║ Positional Or Keyword ║
║ untyped  ║ 4       ║ Any   ║ Positional Or Keyword ║
║ kw_only  ║ 'blue'  ║ str   ║ Keyword Only          ║
╚══════════╩═════════╩═══════╩═══════════════════════╝
```

### Class

On Classes (Not instances), the constructor is also printed.

```python
from explore import explore as ex
import requests
ex(requests.Request)
```
```
  Description:
A user-created :class:`Request <Request>` object.
╔ type: Request ══╦══════╗
║ Functions       ║ Ops  ║
╠═════════════════╬══════╣
║ deregister_hook ║ !=   ║
║ prepare         ║ <    ║
║ register_hook   ║ ==   ║
║                 ║ >    ║
║                 ║ hash ║
╚═════════════════╩══════╝
  Description:
Initialize self.
╔══════════╦═════════╗
║ Argument ║ Default ║
╠══════════╬═════════╣
║ self     ║ ---     ║
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
from explore import explore as ex
import fractions
ex(fractions.Fraction)
```
```
  Description:
This class implements rational numbers.
╔ ABCMeta: Fraction ═══════════════╦═══════════════════════╦════════╗
║ Methods      ║ Functions         ║ Data                  ║ Ops    ║
╠══════════════╬═══════════════════╬═══════════════════════╬════════╣
║ from_decimal ║ as_integer_ratio  ║ denominator: property ║ !=     ║
║ from_float   ║ conjugate         ║ imag: property        ║ %      ║
║              ║ limit_denominator ║ numerator: property   ║ *      ║
║              ║                   ║ real: property        ║ **     ║
║              ║                   ║                       ║ +      ║
║              ║                   ║                       ║ +()    ║
║              ║                   ║                       ║ -      ║
║              ║                   ║                       ║ -()    ║
║              ║                   ║                       ║ /      ║
║              ║                   ║                       ║ //     ║
║              ║                   ║                       ║ <      ║
║              ║                   ║                       ║ ==     ║
║              ║                   ║                       ║ >      ║
║              ║                   ║                       ║ abs    ║
║              ║                   ║                       ║ divmod ║
║              ║                   ║                       ║ float  ║
║              ║                   ║                       ║ hash   ║
║              ║                   ║                       ║ round  ║
╚══════════════╩═══════════════════╩═══════════════════════╩════════╝
  Description:
Initialize self.
╔ Constructor __init__ ════════════════╗
║ Argument ║ Default ║ Kind            ║
╠══════════╬═════════╬═════════════════╣
║ self     ║ ---     ║ Positional Only ║
║ args     ║ ---     ║ Var Positional  ║
║ kwargs   ║ ---     ║ Var Keyword     ║
╚══════════╩═════════╩═════════════════╝
```

## Automatic import
If you have ipython, you can create a file in `~/.ipython/profile_default/startup/` that imports it,
it will then be available at the start of ipython. More explanation [here](https://towardsdatascience.com/how-to-automatically-import-your-favorite-libraries-into-ipython-or-a-jupyter-notebook-9c69d89aa343).
