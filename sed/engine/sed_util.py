#!/usr/bin/env python
from itertools import count
import doctest


def delete_range(lines, r=None):
    """
    >>> a = list(range(10))
    >>> delete_range(a, (1, 3))
    [0, 4, 5, 6, 7, 8, 9]
    """
    r = r or (0, len(lines))
    return replace_range(lines, [], (r[0], r[1] + 1))


def insert_range(lines, line_no, new_lines):
    """
    >>> a = list(range(10))
    >>> b = list(range(11, 13))
    >>> insert_range(a, 3, b)
    [0, 1, 2, 11, 12, 3, 4, 5, 6, 7, 8, 9]
    >>> insert_range(a, 0, b)
    [11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> insert_range(a, 9, b)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 9]
    """
    return replace_range(lines, new_lines, (line_no, line_no))


def append_range(lines, line_no, new_lines):
    """
    >>> a = list(range(10))
    >>> b = list(range(11, 13))
    >>> append_range(a, 3, b)
    [0, 1, 2, 3, 11, 12, 4, 5, 6, 7, 8, 9]
    >>> append_range(a, 0, b)
    [0, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> append_range(a, 9, b)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
    """
    return replace_range(lines, new_lines, (line_no + 1, line_no + 1))


def replace_range(old_lines, new_lines, r=None):
    """
    >>> a = list(range(10))
    >>> b = list(range(11, 13))
    >>> replace_range(a, b, (0, 2))
    [11, 12, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> replace_range(a, b, (8, 10))
    [0, 1, 2, 3, 4, 5, 6, 7, 11, 12]
    >>> replace_range(a, b, (0, 10))
    [11, 12]
    >>> replace_range(a, [], (0, 10))
    []
    >>> replace_range(a, [], (0, 9))
    [9]
    """
    start, end = r or (0, len(old_lines))
    assert 0 <= start <= end <= len(old_lines)
    return old_lines[:start] + new_lines + old_lines[end:]


def find_line(lines, regex):
    for i, line in enumerate(lines):
        m = regex.match(line)
        if m:
            yield i, m.groupdict()


def find_any_line(lines, regexes):
    for regex in regexes:
        i, m = find_line(lines, regex)
        if m:
            yield i, m


def add_terminator(lines, terminator):
    def terminator_gen(last_lineno, terminator):
        for i in count():
            yield terminator if i != last_lineno else ""
    return [line + sep
            for line, sep in zip(lines, terminator_gen(len(lines) - 1, terminator))]


def comma_terminate(lines):
    """
    >>> a = ["a", "b", "c"]
    >>> comma_terminate(a)
    ['a,', 'b,', 'c']
    """
    return add_terminator(lines, ",")


def entab(lines, space_count=4):
    return [line.replace("\t", " " * space_count) for line in lines]


def sort_range(lines, r=None):
    """
    >>> a = sorted(range(10), reverse=True)
    >>> sort_range(a, (1, 1))
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> sort_range(a, (1, 2))
    [9, 7, 8, 6, 5, 4, 3, 2, 1, 0]
    >>> sort_range(a, (0, 2))
    [7, 8, 9, 6, 5, 4, 3, 2, 1, 0]
    >>> sort_range(a)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> sort_range(a, (0, 5))
    [4, 5, 6, 7, 8, 9, 3, 2, 1, 0]
    """
    start, end = r or (0, len(lines))
    return lines[:start] + sorted(lines[start: end + 1]) + lines[end + 1:]


if __name__ == '__main__':
    doctest.testmod()
