#!/usr/bin/env python

import re

from engine import (
    StreamEditor,
    call_main,
    ACCEPT, NEXT, REPEAT
)

APP_GET = re.compile(r'''
    ^
    (?P<leading_space>\s+)
    (?P<assign>.*)
    (?P<app_get>self.app.get)
    (?P<content>.*)
    $
''', re.VERBOSE)

ANY = re.compile(r'''
    ^
    \s+
    (?P<content>.*)
    $
''', re.VERBOSE)


def test_function(matches, args):
    result = "".join([m.get('content', "") for m in matches['matches']])
    result += args['content']
    parens = result.count('(') - result.count(')')
    brackets = result.count('[') - result.count(']')
    braces = result.count('{') - result.count('}')
    if not sum([parens, brackets, braces]):
        return ACCEPT
    elif matches['matches']:
        return REPEAT
    else:
        return NEXT


class StreamEditorRewriteAppGet(StreamEditor):
    table = [
        [[APP_GET, test_function], ], 
        [[ANY, test_function], ],
    ]

    def apply_match(self, i, dict_matches):
        matches = dict_matches['matches']
        first = matches[0]
        leading = first['leading_space']
        tabs = len(leading) / 4
        prefix = '\t' * (tabs + 1)
        content = [first['content'][1:]] + [m['content'] for m in matches[1:]]
        result = [leading + first['assign'] + first['app_get'] + '('] + \
            [prefix + c for c in content]
        loc = (dict_matches["start"], dict_matches["end"] + 1)
        self.replace_range(loc, result)
        self.entab()


if __name__ == '__main__':
    call_main(StreamEditorRewriteAppGet)
