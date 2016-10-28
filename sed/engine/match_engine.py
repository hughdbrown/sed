#!/usr/bin/env python
from __future__ import print_function

from sys import stderr

ACCEPT, REJECT, NEXT, REPEAT = -1, -2, -3, -4
STATE_NAME = {
    ACCEPT: "ACCEPT",
    REJECT: "REJECT",
    NEXT: "NEXT",
    REPEAT: "REPEAT",
}

FMTS = {
    REPEAT: "REPEAT(line {i}, state {state}: --> {state}: {line})\n",
    NEXT: "CONTINUE(line {i}, state {state}: --> {new_state_name}: %{line})\n",
    ACCEPT: "ACCEPT(line {i}, state {state}: {line})\n",
    REJECT: "REJECT(line {i}, state {state}: {line})\n",
    0: "CONTINUE(line {i}, state {state} --> {new_state_name}: {line})\n",
}

MATCH_FMT = "Match(line {i}, state {state} --> {new_state_name}: {line})\n"


def match_engine(lines, regex_specs, verbose=False):
    state = 0
    matches = []
    for i, line in enumerate(lines):
        regex_spec = regex_specs[state]
        # Try to match a regular expression from the current state
        for regex, new_state in regex_spec:
            match = regex.match(line)
            if match:
                if state == 0:
                    matches.append({'start': i, 'end': None, 'matches': []})

                if verbose:
                    # pylint: disable=W0612
                    new_state_name = STATE_NAME.get(new_state, str(new_state))
                    stderr.write(MATCH_FMT.format(i=i, state=state, new_state_name=new_state_name, line=line))
                    fmt = FMTS.get(new_state) or FMTS[0]
                    msg = fmt.format(i=i, state=state, new_state_name=new_state_name, line=line)
                    stderr.write(msg)

                args = dict([('line_no', i)] + match.groupdict().items())

                if hasattr(new_state, '__call__'):
                    new_state = new_state(matches[-1], args)

                if new_state != REJECT:
                    matches[-1]['matches'].append(args)
                if new_state == ACCEPT:
                    matches[-1]['end'] = i
                elif new_state == REJECT:
                    matches = matches[:-1]

                state = (
                    0 if new_state in (ACCEPT, REJECT) else
                    (state + 1) if new_state == NEXT else
                    state if new_state == REPEAT else
                    new_state
                )
                break
            elif verbose:
                print("No match: {0}".format(line))
    return matches
