"""Convert the DoubleTable in the readme file to an ascii table for consistent rendering."""

import terminaltables


def main():
    """Translate table border symbols to ascii table."""
    a = [getattr(terminaltables.AsciiTable, x) for x in dir(terminaltables.AsciiTable) if x.startswith("CHAR_")]
    b = [getattr(terminaltables.DoubleTable, x) for x in dir(terminaltables.DoubleTable) if x.startswith("CHAR_")]
    trans = {ord(a_): b_ for a_, b_ in zip(b, a)}
    with open("README_doubletable.md", encoding="utf8") as infile:
        with open("README.md", "w", encoding="utf8") as outfile:
            outfile.write(infile.read().translate(trans))


if __name__ == "__main__":
    main()
