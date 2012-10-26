import re

# (function () {
ANONYMOUS_FUNCTION = re.compile(r'''
    ^\(function\s+\(\)\s+\{
''', re.VERBOSE)


#         domEvents : _.extend({}, someExisting events, {
EXTEND_DECL = re.compile(r'''
    \s+
    (?P<decl>[\w\d_\$]+?[Ee]vents)
    \s*
    \:
    \s*
    _\.extend\(
    (?P<extend>[\w\d\s\.\{\}_,\$]+?)
    ,
    \s*
    \{
    \s*$
''', re.VERBOSE)

#         domEvents : {
#         postScoringEvents : {
EVENT_DECL = re.compile(r'''
    \s+
    (?P<decl>[\w\d_\$]+?[Ee]vents)
    \s*
    \:
    \s*
    \{
    \s*$
''', re.VERBOSE)

# It turns out to be way easier to match selectors reliably if we use
# the name of the known events at the start of the selector-regex
EVENT_SELECTOR = r'''(click|orientationchange|taphold|''' \
                 '''touch(start|move|end)|''' \
                 '''mouse(move|down|up|leave))'''

# 'click .vocab_answer_button' : '_answerButtonClickedHandler',
SELECTOR = re.compile(r'''
    \s+
    (?P<selector>[\'\"]
''' + EVENT_SELECTOR + r'''
    [\w\d\s\._\#\(\)\:\$]+[\'\"])
    \s*\:
    \s+
    [\'\"]
    (?P<function>[\w\d_\$]+)
    [\'\"]
    ,?
''', re.VERBOSE)

# },
END_DECL = re.compile(r'''
    \s+
    (?P<end_decl>\},?)
''', re.VERBOSE)

# };
END_VAR_DECL = re.compile(r'''
    \s+
    (?P<end_decl>\};)
''', re.VERBOSE)

# We need a runtime method in which to do the _.extend(this._domEvents),
# and hanging it off the initialize method is the best way.
#         initialize : function (options) {
INITIALIZE_MATCH = re.compile(r'''
    ^\s+
    initialize
    \s*\:\s*
    function
    \s*
    \(
    (?P<arg_list>[\w\d\s_,\$]*)
    \)
    \s*
    \{
''', re.VERBOSE)

#         _startTimedMode : function () {
#         _startTimedMode : function (a, b, c) {
FUNCTION_HEADER = re.compile(r'''
    ^
    (?P<leading_space>\s+)
    (?P<function_header>[\w\d_\$]+)
    \s*
    \:
    \s*
    function
    \s*
    \(
    (?P<arg_list>[\w\d\s,_\$]*)
    \)
    (?P<rest>.*)
    $
''', re.VERBOSE)

# var stopEvents = {
VAR_DECL = re.compile(r'''
    ^
    \s+
    var
    \s*
    (?P<var_decl>[\w\d_]*?[Ee]vents)
    \s*
    \=
    \s*
    \{
    \s*$
''', re.VERBOSE)

# stopEvents : {
# stopEvents : function () {
OBJECT_MEMBER_DECL = re.compile(r'''
    ^
    (?P<leading_space>\s+)
    (?P<obj_member_decl>[\w\d_\$]+)
    \s*
    \:
    \s*
    (?P<rest>.*)
    $
''', re.VERBOSE)

# A class by parent_class.extend
# wgen.assess.lib = wgen.assess.extend(
WGEN_CLASS = re.compile(r'''
    (?P<leading_space>.*?)
    (?P<class>wgen\.assess(\.[\w\d\$_]+)+)
    \s?=\s?
    (?P<parent_class>[\w\d\._\$]+?)
    \.extend\(
    (?P<trailing>.*)
''', re.VERBOSE)

# A classic javascript constructor
# wgen.assess.lib = function () {
WGEN_FUNCTION = re.compile(r'''
    ^
    (?P<class>wgen\.assess(\.[\w\d\$_]+)+)
    \s?=\s?
    function\s+\(.*?\)
    \s*
    \{
    \s*
    $
''', re.VERBOSE)

#   var xxx = function (arg1, arg2)
VAR_FUNCTION = re.compile(r'''
    ^
    \s*
    var
    \s*
    (?P<function>[\w\d_]+)
    \s*
    \=
    \s*
    function
    \s*
    \(
    (?P<arg_list>[\w\d\s_,]*)
    \)
    .*
    $
''', re.VERBOSE)

# goog.provide('wgen.assess.lib');
GOOG_PROVIDE = re.compile(r'''
    ^
    goog.provide
    \(
    ['"]
    (?P<class>[\w\d_\$\.]+)
    ['"]
    \)
    ;
''', re.VERBOSE)

# /**
COMMENT_OPEN = re.compile(r'''
    ^
    (?P<leading_space>\s*)
    (?P<comment_open>/\*\*)
    .*
    $
''', re.VERBOSE)

# */
COMMENT_CLOSE = re.compile(r'''
    ^
    (?P<leading_space>\s*)
    (?P<comment_close>\*/)
    .*
    $
''', re.VERBOSE)

BLANK_LINE = re.compile(r'''
    ^
    \s*
    $
''', re.VERBOSE)

ANY = re.compile(r'''
    ^.*$
''', re.VERBOSE)


# Not regexes -- just string constants for replacements
CONSTRUCTOR_FMT = [
    "/**",
    " * @constructor",
    " */",
]

NAMESPACE_FMT = [
    '''%(leading_space)s/**''',
    '''%(leading_space)s * @this {%(namespace)s}''',
    '''%(leading_space)s */''',
]

EXTENDS_FMT = [
    '''%(leading_space)s/**''',
    '''%(leading_space)s * @constructor''',
    '''%(leading_space)s * @extends {%(parent_class)s}''',
    '''%(leading_space)s */''',
]

PRIVATE_FMT = [
    '''%(leading_space)s/**''',
    '''%(leading_space)s * @private''',
    '''%(leading_space)s */''',
]
