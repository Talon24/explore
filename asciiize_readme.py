"""Convert the DoubleTable in the readme file to an ascii table for consistent rendering."""
import io
import re
import contextlib

import terminaltables

import explor


def exec_and_catch_output(match):
    """Execute the code in the match and return the printed output."""
    found = match.group(1)
    stringio = io.StringIO()
    with contextlib.redirect_stdout(stringio):
        explor.COLORIZE = False
        exec(found)
    output = stringio.getvalue()
    return output.rstrip()


def main():
    """Read template Readme file and execute code in the ****...**** blocks. Write output to new files."""
    with open("README_template.md", encoding="utf8") as infile:
        raw = infile.read()
    explor.TABLETYPE = terminaltables.DoubleTable
    with open("README.md", "w", encoding="utf8") as outfile:
        outfile.write(re.sub(r"\*\*\*\*([\s\S]+?)\*\*\*\*", exec_and_catch_output, raw))
    explor.TABLETYPE = terminaltables.AsciiTable
    with open("README_plain.md", "w", encoding="utf8") as outfile:
        outfile.write(re.sub(r"\*\*\*\*([\s\S]+?)\*\*\*\*", exec_and_catch_output, raw))


if __name__ == "__main__":
    main()
