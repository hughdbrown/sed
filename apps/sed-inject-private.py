#!/usr/bin/env python

from engine import (
    StreamEditor,
    call_main,
    ACCEPT
)
from engine.sed_regex import FUNCTION_HEADER, PRIVATE_FMT


# Match all functions in the class
# -----
# Quote the function name of all functions not already quoted
class StreamEditorInjectPrivate(StreamEditor):
    table = [
        [[FUNCTION_HEADER, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        for match in dict_matches["matches"]:
            function_header = match["function_header"]
            if function_header.startswith('_') or function_header.endswith('_'):
                line_no = match["line_no"]
                self.insert_range(line_no, [p % match for p in PRIVATE_FMT])

if __name__ == '__main__':
    call_main(StreamEditorInjectPrivate)
