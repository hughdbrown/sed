#!/usr/bin/env python

import re

from engine import (
    StreamEditor,
    call_main,
    ACCEPT, REPEAT, NEXT,
    ANY
)

# goog.require('wgen.assess.lib');
GOOG_REQUIRE = re.compile(r'''
    ^
    goog.require
    \(
    ['"]
    (?P<class>[\w\d_\$\.]+)
    ['"]
    \)
    ;
''', re.VERBOSE)


class StreamEditorSortGoogRequires(StreamEditor):
    table = [
        [[GOOG_REQUIRE, NEXT], ],
        [[GOOG_REQUIRE, REPEAT], [ANY, ACCEPT]],
    ]

    def apply_match(self, i, dict_matches):
        start, end = dict_matches["start"], dict_matches["end"]
        if not (end is None):
            self.sort_range((start, end - 1))

if __name__ == '__main__':
    call_main(StreamEditorSortGoogRequires)
