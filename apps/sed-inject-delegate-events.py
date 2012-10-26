#!/usr/bin/env python

import re

from engine.StreamEditor import (
    StreamEditor,
    call_main,
    ACCEPT, NEXT
)

PRIVATE_DELEGATE_EVENTS = '''
        /**
         * Replace delegateEvents because it maps strings to functions --
         * a no-no for Closure aggressive compression
         * @private
         */
        _delegateEvents : function (events) {
            var eventSplitter = /^(\w+)\s*(.*)$/;
            events = events || this.events;
            if (events) {
                var element = $(this.el);
                element.unbind();
                for (var key in events) {
                    var method = events[key];
                    var match = key.match(eventSplitter);
                    var eventName = match[1], selector = match[2];
                    if (selector === '') {
                        element.bind(eventName, method);
                    } else {
                        element.delegate(selector, eventName, method);
                    }
                }
            }
        },
'''

DELEGATE_EVENTS_PATCH = '''            this._delegateEvents(events);'''

VIEW = \
    '${ASSESS_HOME}/assess/public/javascript/wgen/assess/common/views/view.js'

# Backbone.View.prototype.delegateEvents.call(this, events);
BACKBONE_DELEGATE_EVENTS_REGEX = re.compile(r'''
    ^
    \s+
    (?P<delegateEvents>Backbone\.View\.prototype\.delegateEvents\.call\(this,
    \s*
    events\);)
''', re.VERBOSE)

PRIVATE_DELEGATE_EVENTS_REGEX = re.compile(r'''
    ^
    \s+
    _delegateEvents
    \s:\s
    function\s+\(events\)
    \s+
    \{
''', re.VERBOSE)

DELEGATE_EVENTS_REGEX = re.compile(r'''
    ^
    \s+
    delegateEvents
    \s:\s
    function\s+\(events\)
    \s+
    \{
''', re.VERBOSE)

END_DECL = re.compile(r'''
    ^
    \s+
    \},
''', re.VERBOSE)


class StreamEditorInjectDelegateEvents(StreamEditor):
    table = [
        [[DELEGATE_EVENTS_REGEX, NEXT], ],
        [[END_DECL, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        start, end = dict_matches["start"], dict_matches["end"]
        assert start <= end

        j, _ = self.find_line(BACKBONE_DELEGATE_EVENTS_REGEX)
        if j is not None:
            assert start <= j <= end
            self.replace_range((j, j + 1), [DELEGATE_EVENTS_PATCH])

        k, _ = self.find_line(PRIVATE_DELEGATE_EVENTS_REGEX)
        if k is None:
            self.insert_range(start, [PRIVATE_DELEGATE_EVENTS])


if __name__ == '__main__':
    #import os.path
    #path = os.path.expandvars(VIEW)
    #call_main([path], StreamEditorInjectDelegateEvents)
    call_main(StreamEditorInjectDelegateEvents)
