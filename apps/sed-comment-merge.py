#!/usr/bin/env python

from engine import (
    StreamEditor,
    call_main,
    ACCEPT, REJECT, NEXT, REPEAT
)
from engine.sed_regex import COMMENT_OPEN, COMMENT_CLOSE, BLANK_LINE, ALL


# Find consecutive jsdoc comments
#   /**
#   ...
#    */
#   /**
#   ...
#    */
# -----
# delete intermediate end and start
class StreamEditorCommentMerge(StreamEditor):
    table = [
        [[COMMENT_OPEN, NEXT], ],
        [[COMMENT_CLOSE, NEXT], ],
        # Allow a new comment or a blank line, but bail otherwise
        [[COMMENT_OPEN, NEXT], [BLANK_LINE, REPEAT], [ALL, REJECT], ],
        [[COMMENT_CLOSE, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        end, matches = dict_matches["end"], dict_matches["matches"]
        if not (end is None):
            delete_start = matches[1]['line_no']
            delete_end = matches[2]['line_no']
            self.delete_range((delete_start, delete_end))

if __name__ == '__main__':
    call_main(StreamEditorCommentMerge)
