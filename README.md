# explore
Python object explorer which shows you what you can do with an object.

It takes the output from `dir()`, checks this and classifies it in a table.
With that, you don't have to read the entire output of `dir()` and visually
filter it for the relevant information.

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


## Installation

Install the package:
`pip install git+git://github.com/Talon24/explore`

## Usage

The module's name is `explore` and it provides a function called `explore()`.
To simplify exploration, i'd recommend aliasing it as something short like `ex`. 

```python
from explore import explore as ex
import pathlib

ex(pathlib)
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

If you have ipython, you can create a file in `~/.ipython/profile_default/startup/` that imports it,
it will then be available at the start of ipython.
