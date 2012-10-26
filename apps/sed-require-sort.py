#!/usr/bin/env python

from engine.StreamEditor import StreamEditor
from engine.sed_regex import \
    GOOG_REQUIRE, ANY
from engine.sed_file_util import call_main
from engine.match_engine import ACCEPT, REPEAT, NEXT


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
