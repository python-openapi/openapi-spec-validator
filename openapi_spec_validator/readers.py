import os
import pathlib
import sys

from jsonschema_spec.handlers import file_handler, all_urls_handler


def read_from_stdin(filename):
    return file_handler(sys.stdin), ''


def read_from_filename(filename):
    if not os.path.isfile(filename):
        raise IOError("No such file: {0}".format(filename))

    filename = os.path.abspath(filename)
    uri = pathlib.Path(filename).as_uri()
    return all_urls_handler(uri), uri
