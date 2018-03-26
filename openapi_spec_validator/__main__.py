import logging
import optparse
import os
import sys

from openapi_spec_validator import validate_spec_url
from openapi_spec_validator.exceptions import ValidationError

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.WARNING
)


def main():
    usage = 'Usage: %prog filename'
    parser = optparse.OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('You must provide a filename to validate')
    filename = args[0]
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
