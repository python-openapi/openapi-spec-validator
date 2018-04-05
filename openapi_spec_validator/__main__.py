import logging
import argparse
import os
import sys

from openapi_spec_validator import validate_spec_url
from openapi_spec_validator.exceptions import ValidationError

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.WARNING
)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="Absolute or relative path to file")
    args = parser.parse_args(args)
    filename = args.filename
    filename = os.path.abspath(filename)
    try:
        validate_spec_url('file://'+filename)
    except ValidationError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(2)
    else:
        print('OK')


if __name__ == '__main__':
    main()
