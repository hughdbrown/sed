#!/usr/bin/env python
import re

from engine import (
    StreamEditor,
    call_main,
    ACCEPT
)
from engine.sed_regex import (
    FUNCTION_HEADER, WGEN_CLASS, WGEN_FUNCTION,
    CONSTRUCTOR_FMT, NAMESPACE_FMT, EXTENDS_FMT
)


VAR_DECL_FMT = r'''
    ^
    \s*
    var
    \s+
    %(parent_class)s
    \s*
    \=
    \s*
    (?P<expanded_parent_class>[\w\d\$\_\.]+)
    ;
'''


# Match all functions in the class
# -----
# Prefix function header with a jsdoc block that declares what 'this' is
# 'this' is discovered by
class StreamEditorInjectNamespace(StreamEditor):
    table = [
        [[FUNCTION_HEADER, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        start, matches = dict_matches["start"], dict_matches["matches"]
        abc = [WGEN_CLASS, WGEN_FUNCTION]
        namespace_i, ns_matches = self.find_any_line(abc)

        if (namespace_i is not None):
            for match in matches:
                args = {
                    'leading_space': match['leading_space'],
                    'namespace': ns_matches['class'],
                }
                new_decl = [fmt % args for fmt in NAMESPACE_FMT]
                self.insert_range(start, new_decl)


class StreamEditorInjectExtends(StreamEditor):
    table = [
        [[WGEN_CLASS, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        start, matches = dict_matches["start"], dict_matches["matches"]
        for match in matches:
            parent_class = match["parent_class"]
            var_decl = re.compile(VAR_DECL_FMT % locals(), re.VERBOSE)
            _, var_decl_match = self.find_line(var_decl)
            expanded_parent_class = \
                var_decl_match.get('expanded_parent_class') if var_decl_match \
                else None
            args = {
                'leading_space': match['leading_space'],
                'parent_class': expanded_parent_class or parent_class,
            }
            self.insert_range(start, [e % args for e in EXTENDS_FMT])


class StreamEditorInjectContructor(StreamEditor):
    table = [
        [[WGEN_FUNCTION, ACCEPT], ],
    ]

    def apply_match(self, i, dict_matches):
        self.insert_range(dict_matches["start"], CONSTRUCTOR_FMT)


if __name__ == '__main__':
    StreamEditors = [
        StreamEditorInjectNamespace,
        StreamEditorInjectContructor,
        StreamEditorInjectExtends,
    ]
    for streamEditor in StreamEditors:
        call_main(streamEditor)
