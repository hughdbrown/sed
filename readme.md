## What is sed?

sed is a streaming editor toolkit written in python. It is used to make programs that modify code.

## Installation

```shell
git clone ssh://git@github.com:hughdbrown/sed.git
cd sed
python setup.py install
```

## Documentation

The basic idea is that you define a class derived from `StreamEditor`
that describes the regular expressions you wish to capture and act on.

Here is an example:

```python
class StreamEditorSortGoogRequires(StreamEditor):
    table = [
        [[GOOG_REQUIRE, NEXT], ],
        [[GOOG_REQUIRE, REPEAT], [ANY, ACCEPT]],
    ]

    def apply_match(self, i, dict_matches):
        start, end = dict_matches["start"], dict_matches["end"]
        if not (end is None):
            self.sort_range((start, end - 1))
```

This defines a table of transitions and a function to apply
to a match that is found. The engine repeatedly tries the current
regular expression until it finds a match. In this case, that is 
the `GOOG_REQUIRE` regular expression. Once it finds the match,
it goes to the `NEXT` state, which means that it transitions to 
trying the next regular expression. If it finds another `GOOG_REQUIRE`,
then it stays in the current state and continues to capture lines.
If not, then it accepts the series of captures and resets the current
state to the first line in the table.

Essentially, this table defines capturing a consecutive sequence
of one of more `GOOG_REQUIRE` lines.

Once the engine has run over all the lines, it invokes the user-defined
`apply_match` method. It allows users to modify lines within the range of
lines captured. In this case, the user is sorting the lines in alphabetical
order. Effectively, this makes a sequence of `GOOG_REQUIRE` lines get
rewritten in sorted order.

## Platform Support

sed runs on python 2.6, 2.7, 3.1, 3.2, 3.4, 3.5, and pypy.
The tools it uses to build and test do not work on
python 3.1, but otherwise it is fine.

## About

Version 1 of the project features the combined efforts of:

* [Hugh Brown](http://iwebthereforeiam.com)

