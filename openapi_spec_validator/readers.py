import sys
from os import path
from pathlib import Path
from typing import Tuple

from jsonschema_path.handlers import all_urls_handler
from jsonschema_path.handlers import file_handler
from jsonschema_path.typing import Schema


def read_from_stdin(filename: str) -> Tuple[Schema, str]:
    return file_handler(sys.stdin), ""  # type: ignore


def read_from_filename(filename: str) -> Tuple[Schema, str]:
    if not path.isfile(filename):
        raise OSError(f"No such file: {filename}")

    filename = path.abspath(filename)
    uri = Path(filename).as_uri()
    return all_urls_handler(uri), uri
