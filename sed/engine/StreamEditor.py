#!/usr/bin/env python
from __future__ import print_function

import sys
import os.path

from sed.engine.match_engine import match_engine
from sed.engine.sed_util import (
    delete_range, insert_range, append_range, replace_range,
    find_line, find_any_line,
    entab,
    sort_range
)


# The interface for a class derived from StreamEditor is that it
# (1) define self.table at class scope
# (2) override apply_match with a method that will apply transformations
# to self.lines using the information in a match
class StreamEditor(object):
    """
    Abstract class for stream editing
    """
    table = []  # Must be overridden in derived scope

    def __init__(self, filename, options):
        if not self.table:
            # Derived class provides an implementation
            raise NotImplementedError("StreamEditor.table")
        self.changes = 0
        self.verbose = options.verbose
        self.dryrun = options.dryrun
        base, _ = os.path.splitext(filename)
        self.new_filename = (
            None if not options.new_ext
            else base + options.new_ext
        )
        self.filename = filename
        with open(self.filename) as handle:
            self.lines = [line.rstrip() for line in handle]
            self.matches = list(reversed(self.match_engine()))

    def transform(self):
        for i, dict_matches in enumerate(self.matches):
            self.apply_match(i, dict_matches)

    def apply_match(self, i, dict_matches):
        # Derived class provides an implementation
        raise NotImplementedError("StreamEditor.apply_match")

    def save(self):
        if self.changes:
            filename = self.new_filename or self.filename
            if self.verbose:
                msg = "Saving {o.filename} to {0}: {o.changes} changes\n".format(filename, o=self)
                sys.stderr.write(msg)
            with open(filename, "w") as handle:
                handle.write("\n".join(self.lines) + "\n")
            self.changes = 0

    def match_engine(self):
        return match_engine(self.lines, self.table, self.verbose)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def copy_range(self, loc):
        start, end = loc
        return self.lines[start:end]

    def replace_range(self, loc, new_lines):
        self.lines = replace_range(self.lines, new_lines, loc)
        self.changes += 1

    def insert_range(self, loc, new_lines):
        self.lines = insert_range(self.lines, new_lines, loc)
        self.changes += 1

    def append_range(self, loc, new_lines):
        self.lines = append_range(self.lines, new_lines, loc)
        self.changes += 1

    def delete_range(self, loc):
        self.lines = delete_range(self.lines, loc)
        self.changes += 1

    def entab(self):
        self.lines = entab(self.lines)
        self.changes += 1

    def find_line(self, regex, lines=None):
        lines = lines or self.lines
        return find_line(lines, regex)

    def find_any_line(self, regexes, lines=None):
        lines = lines or self.lines
        return find_any_line(lines, regexes)

    def sort_range(self, loc):
        self.lines = sort_range(self.lines, loc)
        self.changes += 1
