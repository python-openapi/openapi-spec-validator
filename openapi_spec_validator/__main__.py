import logging
import sys
from argparse import ArgumentParser
from typing import Optional
from typing import Sequence

from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import best_match

from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator.readers import read_from_stdin
from openapi_spec_validator.shortcuts import validate
from openapi_spec_validator.validation import OpenAPIV2SpecValidator
from openapi_spec_validator.validation import OpenAPIV30SpecValidator
from openapi_spec_validator.validation import OpenAPIV31SpecValidator

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.WARNING,
)


def print_ok(filename: str) -> None:
    print(f"{filename}: OK")


def print_error(filename: str, exc: Exception) -> None:
    print(f"{filename}: Error: {exc}")


def print_validationerror(
    filename: str, exc: ValidationError, errors: str = "best-match"
) -> None:
    print(f"{filename}: Validation Error: {exc}")
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
    parser.add_argument(
        "file",
        nargs="+",
        help="Validate specified file(s).",
    )
    parser.add_argument(
        "--errors",
        choices=("best-match", "all"),
        default="best-match",
        help="""Control error reporting. Defaults to "best-match", """
        """use "all" to get all subschema errors.""",
    )
    parser.add_argument(
        "--schema",
        type=str,
        choices=["detect", "2.0", "3.0", "3.1", "3.0.0", "3.1.0"],
        default="detect",
        metavar="{detect,2.0,3.0,3.1}",
        help="OpenAPI schema version (default: detect).",
    )
    args_parsed = parser.parse_args(args)

    for filename in args_parsed.file:
        # choose source
        reader = read_from_filename
        if filename in ["-", "/-"]:
            filename = "stdin"
            reader = read_from_stdin

        # read source
        try:
            spec, base_uri = reader(filename)
        except Exception as exc:
            print(exc)
            sys.exit(1)

        # choose the validator
        validators = {
            "detect": None,
            "2.0": OpenAPIV2SpecValidator,
            "3.0": OpenAPIV30SpecValidator,
            "3.1": OpenAPIV31SpecValidator,
            # backward compatibility
            "3.0.0": OpenAPIV30SpecValidator,
            "3.1.0": OpenAPIV31SpecValidator,
        }
        validator_cls = validators[args_parsed.schema]

        # validate
        try:
            validate(spec, base_uri=base_uri, cls=validator_cls)
        except ValidationError as exc:
            print_validationerror(filename, exc, args_parsed.errors)
            sys.exit(1)
        except Exception as exc:
            print_error(filename, exc)
            sys.exit(2)
        else:
            print_ok(filename)


if __name__ == "__main__":
    main()
