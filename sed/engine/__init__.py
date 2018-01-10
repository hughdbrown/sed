"""
Interface to sed engine
- defines objects exported from this module
"""
from sed.engine.StreamEditor import StreamEditor
from sed.engine.sed_file_util import call_main
from sed.engine.match_engine import (
    ACCEPT,
    REJECT,
    NEXT,
    REPEAT,
    CUT,
)
from sed.engine.sed_regex import ANY


__all__ = [
    "StreamEditor",
    "call_main",
    "ACCEPT", "REJECT", "NEXT", "REPEAT", "CUT",
    "ANY",
]
