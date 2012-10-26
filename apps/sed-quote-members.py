#!/usr/bin/env python

from engine import (
    StreamEditor,
    call_main,
    ACCEPT
)
from engine.sed_regex import FUNCTION_HEADER

FMT = """%(leading_space)s'%(function_header)s' : """ \
      """function (%(arg_list)s) %(rest)s"""


# Match all functions in the class
# -----
# Quote the function name of all functions not already quoted
class StreamEditorQuoteFunctions(StreamEditor):
    table = [
        [[FUNCTION_HEADER, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        end, matches = dict_matches["end"], dict_matches["matches"]
        if (end is not None):
            for match in matches:
                line_no = match["line_no"]
                self.replace_range((line_no, line_no + 1), [FMT % match])


if __name__ == '__main__':
    call_main(StreamEditorQuoteFunctions)
