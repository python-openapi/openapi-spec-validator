import logging
import sys
from argparse import ArgumentParser
from typing import Optional
from typing import Sequence

from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import best_match

from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator.readers import read_from_stdin
from openapi_spec_validator.validation import openapi_spec_validator_proxy
from openapi_spec_validator.validation import openapi_v2_spec_validator
from openapi_spec_validator.validation import openapi_v30_spec_validator
from openapi_spec_validator.validation import openapi_v31_spec_validator

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.WARNING,
)


def print_validationerror(
    exc: ValidationError, errors: str = "best-match"
) -> None:
    print("# Validation Error\n")
    print(exc)
    if exc.cause:
        print("\n# Cause\n")
        print(exc.cause)
    if not exc.context:
        return
    if errors == "all":
        print("\n\n# Due to one of those errors\n")
        print("\n\n\n".join("## " + str(e) for e in exc.context))
    elif errors == "best-match":
        print("\n\n# Probably due to this subschema error\n")
        print("## " + str(best_match(exc.context)))
        if len(exc.context) > 1:
            print(
                f"\n({len(exc.context) - 1} more subschemas errors,",
                "use --errors=all to see them.)",
            )


def main(args: Optional[Sequence[str]] = None) -> None:
    parser = ArgumentParser()
    parser.add_argument("filename", help="Absolute or relative path to file")
    parser.add_argument(
        "--errors",
        choices=("best-match", "all"),
        default="best-match",
        help="""Control error reporting. Defaults to "best-match", """
        """use "all" to get all subschema errors.""",
    )
    parser.add_argument(
        "--schema",
        help="OpenAPI schema (default: detect)",
        type=str,
        choices=["2.0", "3.0.0", "3.1.0", "detect"],
        default="detect",
    )
    args_parsed = parser.parse_args(args)

    # choose source
    reader = read_from_filename
    if args_parsed.filename in ["-", "/-"]:
        reader = read_from_stdin

    # read source
    try:
        spec, spec_url = reader(args_parsed.filename)
    except Exception as exc:
        print(exc)
        sys.exit(1)

    # choose the validator
    validators = {
        "2.0": openapi_v2_spec_validator,
        "3.0.0": openapi_v30_spec_validator,
        "3.1.0": openapi_v31_spec_validator,
        "detect": openapi_spec_validator_proxy,
    }
    validator = validators[args_parsed.schema]

    # validate
    try:
        validator.validate(spec, spec_url=spec_url)
    except ValidationError as exc:
        print_validationerror(exc, args_parsed.errors)
        sys.exit(1)
    except Exception as exc:
        print(exc)
        sys.exit(2)
    else:
        print("OK")


if __name__ == "__main__":
    main()
