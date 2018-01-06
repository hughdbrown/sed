#!/usr/bin/env python
import os
from os.path import isdir, splitext
from optparse import make_option, OptionParser
import logging

# pylint: disable=logging-format-interpolation
logging.basicConfig(level=logging.getLevelName(os.getenv("LOGCFG", "WARNING")))
LOGGER = logging.getLogger(__name__)


def call_main(StreamEditorClass):
    # Given a directory root and a file extension, find all the
    # files that match down that directory tree
    # Returns a generator, not a list
    def pathiter(start_dir, ext=None):
        LOGGER.info("start_dir is {0}".format(start_dir))
        LOGGER.info("ext is {0}".format(ext))
        return (
            os.path.normpath(os.path.join(root, f))
            for root, _, files in os.walk(start_dir)
            for f in files
            if not ext or (splitext(f)[1] == ext)
        )

    def main(filename, StreamEditorClass, options):
        try:
            with StreamEditorClass(filename, options) as streamed:
                streamed.transform()
        except IOError:
            LOGGER.exception("sed_file_util:main({0})".format(filename))

    option_list = [
        make_option('-d', '--dry-run', dest="dryrun", action="store_true",
                    default=False, help="Execute commands or just do dry run"),
        make_option('-e', '--ext', dest="extension",
                    default=None, help="Extension to operate on (.ext)"),
        make_option('-n', '--new-ext', dest="new_ext",
                    default=None, help="Extension to use in renaming file (.ext)"),
        make_option('-v', '--verbose', dest="verbose", action="store_true",
                    default=False, help="Verbose output"),
    ]
    parser = OptionParser(option_list=option_list, add_help_option=True)
    options, args = parser.parse_args()

    args = args or ["."]
    for arg in args:
        if isdir(arg):
            for path in pathiter(arg, options.extension):
                main(path, StreamEditorClass, options)
        else:
            main(arg, StreamEditorClass, options)
