#!/usr/bin/env python

import re

from engine import (
    StreamEditor,
    call_main,
    ACCEPT
)

VIEW = \
    '${ASSESS_HOME}/assess/public/javascript/wgen/assess/common/views/view.js'

PRIVATE_DELEGATE_EVENTS_REGEX = re.compile(r'''
    ^
    \s+
    _delegateEvents
    \s:\s
    function\s+\(events\)
    \s+
    \{
''', re.VERBOSE)

BACKBONE_PATCH = [
    "\t\t\tBackbone.View.prototype.delegateEvents.call(this, events);",
    "\t\t\treturn;",
]


class StreamEditorRevertDelegateEvents(StreamEditor):
    table = [
        [[PRIVATE_DELEGATE_EVENTS_REGEX, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        self.append_range(dict_matches["start"], BACKBONE_PATCH)
        self.entab()


if __name__ == '__main__':
    #import os.path
    #path = os.path.expandvars(VIEW)
    #call_main([path], StreamEditorRevertDelegateEvents)
    call_main(StreamEditorRevertDelegateEvents)
