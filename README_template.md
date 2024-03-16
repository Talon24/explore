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
****
import datetime
print(dir(datetime.datetime.now()))
****
```

To this

```python
from explor import explore as ex
import datetime

ex(datetime.datetime.now())
```
```
****
import datetime
explor.explore(datetime.datetime.now())
****
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
Also, text output is colored by default, but you can disable it with:
```python
import explor
explor.COLORIZE = False
```

### Module

```python
from explor import explore as ex
import pathlib

ex(pathlib)
```
```
****
import pathlib
explor.explore(pathlib)
****
```

### Function

```python
from explor import explore as ex
def a_function(pos: int, /, both: float, untyped=4, *, kw_only: str = "blue") -> complex:
    """Kinds of arguments."""
ex(a_function)
```
```
****
def a_function(pos: int, /, both: float, untyped=4, *, kw_only: str = "blue") -> complex:
    """Kinds of arguments."""
explor.explore(a_function)
****
```

### Class

On Classes (Not instances), the constructor is also printed.

```python
from explor import explore as ex
import requests
ex(requests.Request)
```
```
****
import requests
explor.explore(requests.Request)
****
```

```python
from explor import explore as ex
import fractions
ex(fractions.Fraction)
```
```
****
import fractions
explor.explore(fractions.Fraction)
****
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
