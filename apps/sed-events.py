#!/usr/bin/env python

from engine import (
    StreamEditor,
    call_main,
    ACCEPT, REJECT, NEXT
)
from engine.sed_util import comma_terminate
from engine.sed_regex import \
    END_DECL, END_VAR_DECL, FUNCTION_HEADER, SELECTOR, VAR_DECL


def build_pairs(pairs):
    fmt = "\t\t\t\t%s: $.proxy(this.%s, this)"
    return comma_terminate([fmt % (sel, fn) for sel, fn in pairs])


#Match events declared as a variable within a function
#
#       var setEndingScreenEvents = {
#           "click  #onEndBracket"           : "_onEndBracketButtonClickHandler",
#           "click  .progmon_cancel_button"  : "_cancelButtonSetEndingScreen",
#           "click  .progmon_ok_button"      : "_endingOkButtonClickHandler"
#       };
# -----
# modify in place
class StreamEditorModifyEventsWithinMethod(StreamEditor):
    table = [
        [[FUNCTION_HEADER, NEXT], ],
        [[VAR_DECL, NEXT], [END_DECL, REJECT], ],
        [[SELECTOR, 2], [END_VAR_DECL, NEXT], ],
        [[VAR_DECL, 2], [END_DECL, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        end, matches = dict_matches["end"], dict_matches["matches"]
        assert not (end is None)
        # Discard function header and closing end_decl
        events = matches[1:-1]
        # var_decl and end_decl must be balanced
        var_starts = [i for i, e in enumerate(events) if 'var_decl' in e]
        var_ends = [i for i, e in enumerate(events) if 'end_decl' in e]
        assert len(var_starts) == len(var_ends)
        for v_start, v_end in zip(var_starts, var_ends):
            var_events = events[v_start + 1: v_end]
            if var_events:
                new_lines = build_pairs([
                    (ve["selector"], ve["function"])
                    for ve in var_events])
                loc = (var_events[0]["line_no"], \
                    var_events[-1]["line_no"] + 1)
                self.replace_range(loc, new_lines)
                self.entab()

if __name__ == '__main__':
    call_main(StreamEditorModifyEventsWithinMethod)
