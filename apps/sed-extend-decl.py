#!/usr/bin/env python
from sys import stderr

from engine import (
    StreamEditor,
    call_main,
    ACCEPT, NEXT, REPEAT
)
from engine.sed_regex import END_DECL, EXTEND_DECL, INITIALIZE_MATCH, SELECTOR
from engine.sed_util import comma_terminate


def build_pairs(pairs):
    fmt = "\t\t\t\t%s: $.proxy(this.%s, this)"
    return comma_terminate([fmt % (sel, fn) for sel, fn in pairs])


def build_newlines(decl, pairs):
    return ["\t\t\tthis.%s = _.extend(this.%s, {" % (decl, decl)] + \
        build_pairs(pairs) + \
        ["\t\t\t});"]


# Match a domEvents initialization by extension:
#       _domEvents : _.extend({}, wgen.assess.common.views.ClasseListView.prototype._domEvents, {
#           'click #compositeScore' : '_compositeScoreSortHandler',
#           'click #readingLevel' : '_readingLevelSortHandler',
#           'change #class_list_dropdown_row' : '_changeScoreSortHandler'
#       }),
# -----
# replace original events with only extension of existing events
# move hard-coded events to initialize
class StreamEditorExtendEventsDecl(StreamEditor):
    table = [
        [[EXTEND_DECL, NEXT], ],
        [[SELECTOR, REPEAT], [END_DECL, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        start, end, matches = \
            dict_matches["start"], dict_matches["end"], dict_matches["matches"]
        if not (end is None):
            decl = matches[0]["decl"]
            extend = matches[0]["extend"]
            events = matches[1:-1]
            pairs = [(event["selector"], event["function"]) for event in events]
            new_lines = build_newlines(decl, pairs)
            new_event = "\t\t%s: _.extend(%s)," % (decl, extend)
            initialize, _ = self.find_line(INITIALIZE_MATCH)
            if initialize is not None:
                if start < initialize:
                    self.append_range(initialize, new_lines)
                    self.replace_range((start, end + 1), [new_event])
                else:
                    self.replace_range((start, end + 1), [new_event])
                    self.append_range(initialize, new_lines)
                self.entab()
            else:
                stderr.write("*** %s: missing initialize\n" % self.filename)
        else:
            stderr.write("%s: match started at %d\n" % (self.filename, start),
                         matches)


if __name__ == '__main__':
    call_main(StreamEditorExtendEventsDecl)
