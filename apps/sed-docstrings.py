#!/usr/bin/env python

from sys import stderr
import re

from engine import (
    StreamEditor,
    call_main,
    ACCEPT, REJECT, NEXT, REPEAT,
    ANY
)

FN_DECL_FMT = re.compile(r'''
    ^
    \s*
    def\s+test.+
    $
''', re.VERBOSE)

DOCSTRING_FMT = re.compile(r'''
    ^
    (?P<indent>\s*)
    """
    (?P<content>[^"]*?)
    """
    $
''', re.VERBOSE)

DOCSTRING_START = re.compile(r'''
    ^
    (?P<indent>\s*)
    \"\"\"
    (?P<content>.*?)
    $
''', re.VERBOSE)

CONTENT = re.compile(r'''
    ^
    (?P<indent>\s*)
    (?P<content>.*?)
    $
''', re.VERBOSE)

DOCSTRING_END = re.compile(r'''
    ^
    (?P<indent>\s*)
    (?P<content>.*?)
    \"\"\"
    $
''', re.VERBOSE)


class StreamEditorDocstring(StreamEditor):
    """
    Implementation-inheritance of apply_match
    """
    def __init__(self, filename, verbose=False):
        StreamEditor.__init__(self, filename, verbose)

    def apply_match(self, i, dict_matches):
        end, matches = dict_matches["end"], dict_matches["matches"][1:]
        if matches and not (end is None):
            replace_start = matches[0]['line_no']
            replace_end = matches[-1]['line_no']
            fmt = '%(indent)s# %(content)s'
            changes = [(fmt % match).rstrip() for match in matches]
            if not self.dryrun:
                self.replace_range((replace_start, replace_end + 1), changes)
            if self.verbose or self.dryrun:
                stderr.write("%s\n" % ('-' * 30))
                stderr.write("(%d %d) %s\n" % \
                             (replace_start, replace_end, self.filename))
                stderr.write("\n".join(changes) + "\n")


class StreamEditorDocstringMulti(StreamEditorDocstring):
    """
    Stream editor for multi-line docstrings
    """
    table = [
        [[FN_DECL_FMT, NEXT], ],
        [[DOCSTRING_START, NEXT], [ANY, REJECT], ],
        [[DOCSTRING_END, ACCEPT], [CONTENT, REPEAT], ],
    ]

    def __init__(self, filename, verbose=False):
        StreamEditorDocstring.__init__(self, filename, verbose)


class StreamEditorDocstringSingle(StreamEditorDocstring):
    """
    Stream editor for single line docstrings
    """
    table = [
        [[FN_DECL_FMT, NEXT], ],
        [[DOCSTRING_FMT, ACCEPT], [ANY, REJECT]],
    ]

    def __init__(self, filename, verbose=False):
        StreamEditorDocstring.__init__(self, filename, verbose)


if __name__ == '__main__':
    editors = (StreamEditorDocstringSingle, StreamEditorDocstringMulti, )
    for editor in editors:
        call_main(editor)
