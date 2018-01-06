#!/usr/bin/env python
from __future__ import print_function

import os
import logging

# This disables the pylint warning for logging. I should figure out how to
# do logging messages right.
# pylint: disable=logging-format-interpolation

# This disables the pylint warning for logging. I should figure out how to
# do logging messages right.
# pylint: disable=logging-format-interpolation

ACCEPT, REJECT, NEXT, REPEAT, CUT = -1, -2, -3, -4, -5
STATE_NAME = {
    ACCEPT: "ACCEPT",
    REJECT: "REJECT",
    NEXT: "NEXT",
    REPEAT: "REPEAT",
    CUT: "CUT",
}

FMTS = {
    CUT: "CUT(line {i}, state {state}: --> {state}: {line})\n",
    REPEAT: "REPEAT(line {i}, state {state}: --> {state}: {line})\n",
    NEXT: "CONTINUE(line {i}, state {state}: --> {new_state_name}: %{line})\n",
    ACCEPT: "ACCEPT(line {i}, state {state}: {line})\n",
    REJECT: "REJECT(line {i}, state {state}: {line})\n",
    0: "CONTINUE(line {i}, state {state} --> {new_state_name}: {line})\n",
}

MATCH_FMT = "Match(line {i}, state {state} --> {new_state_name}: {line})\n"

logging.basicConfig(level=logging.getLevelName(os.getenv('LOGCFG', 'WARNING')))
LOGGER = logging.getLogger(__name__)


def match_engine(lines, regex_specs, verbose=False):
    state = 0
    matches = []
    i = 0
    while i < len(lines):
        line = lines[i]
        regex_spec = regex_specs[state]
        # Try to match a regular expression from the current state
        for regex, new_state in regex_spec:
            match = regex.match(line)
            if match:
                if state == 0:
                    LOGGER.debug("New matches starting at {0}".format(i))
                    matches.append({'start': i, 'end': None, 'matches': []})

                if verbose:
                    # pylint: disable=W0612
                    new_state_name = STATE_NAME.get(new_state, str(new_state))
                    kwargs = {
                        'i': i,
                        'state': state,
                        'new_state_name': new_state_name,
                        'line': line,
                    }
                    LOGGER.debug(MATCH_FMT.format(**kwargs))
                    fmt = FMTS.get(new_state) or FMTS[0]
                    LOGGER.debug(fmt.format(**kwargs))

                args = dict([('line_no', i)] + match.groupdict().items())

                if callable(new_state):
                    new_state = new_state(matches[-1], args)

                if new_state == CUT:
                    LOGGER.info("Cutting line '{0}'".format(line))
                    i -= 1

                if new_state not in (REJECT, CUT):
                    matches[-1]['matches'].append(args)
                if new_state in (ACCEPT, CUT):
                    matches[-1]['end'] = i
                elif new_state == REJECT:
                    matches = matches[:-1]

                state = (
                    0 if new_state in (ACCEPT, REJECT, CUT) else
                    (state + 1) if new_state == NEXT else
                    state if new_state == REPEAT else
                    new_state
                )
                break
            elif verbose:
                LOGGER.debug("No match: {0}".format(line))
        i += 1
    return matches
