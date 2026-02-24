import logging
import os
import sys
from argparse import ArgumentParser
from collections.abc import Sequence

from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import best_match

from openapi_spec_validator import __version__
from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator.readers import read_from_stdin
from openapi_spec_validator.shortcuts import get_validator_cls
from openapi_spec_validator.shortcuts import validate
from openapi_spec_validator.validation import OpenAPIV2SpecValidator
from openapi_spec_validator.validation import OpenAPIV30SpecValidator
from openapi_spec_validator.validation import OpenAPIV31SpecValidator
from openapi_spec_validator.validation import SpecValidator

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
    filename: str,
    exc: ValidationError,
    subschema_errors: str = "best-match",
    index: int | None = None,
) -> None:
    if index is None:
        print(f"{filename}: Validation Error: {exc}")
    else:
        print(f"{filename}: Validation Error: [{index}] {exc}")
    if exc.cause:
        print("\n# Cause\n")
        print(exc.cause)
    if not exc.context:
        return
    if subschema_errors == "all":
        print("\n\n# Due to one of those errors\n")
        print("\n\n\n".join("## " + str(e) for e in exc.context))
    elif subschema_errors == "best-match":
        print("\n\n# Probably due to this subschema error\n")
        print("## " + str(best_match(exc.context)))
        if len(exc.context) > 1:
            print(
                f"\n({len(exc.context) - 1} more subschemas errors,",
                "use --subschema-errors=all to see them.)",
            )


def should_warn_deprecated() -> bool:
    return os.getenv("OPENAPI_SPEC_VALIDATOR_WARN_DEPRECATED", "1") != "0"


def warn_deprecated(message: str) -> None:
    if should_warn_deprecated():
        print(f"DeprecationWarning: {message}", file=sys.stderr)


def main(args: Sequence[str] | None = None) -> None:
    parser = ArgumentParser(prog="openapi-spec-validator")
    parser.add_argument(
        "file",
        nargs="+",
        help="Validate specified file(s).",
    )
    parser.add_argument(
        "--subschema-errors",
        choices=("best-match", "all"),
        default=None,
        help="""Control subschema error details. Defaults to "best-match", """
        """use "all" to get all subschema errors.""",
    )
    parser.add_argument(
        "--validation-errors",
        choices=("first", "all"),
        default="first",
        help="""Control validation errors count. Defaults to "first", """
        """use "all" to get all validation errors.""",
    )
    parser.add_argument(
        "--errors",
        "--error",
        dest="deprecated_subschema_errors",
        choices=("best-match", "all"),
        default=None,
        help="Deprecated alias for --subschema-errors.",
    )
    parser.add_argument(
        "--schema",
        type=str,
        choices=["detect", "2.0", "3.0", "3.1", "3.0.0", "3.1.0"],
        default="detect",
        metavar="{detect,2.0,3.0,3.1}",
        help="OpenAPI schema version (default: detect).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args_parsed = parser.parse_args(args)

    subschema_errors = args_parsed.subschema_errors
    if args_parsed.deprecated_subschema_errors is not None:
        if args_parsed.subschema_errors is None:
            subschema_errors = args_parsed.deprecated_subschema_errors
            warn_deprecated(
                "--errors/--error is deprecated. "
                "Use --subschema-errors instead."
            )
        else:
            warn_deprecated(
                "--errors/--error is deprecated and ignored when "
                "--subschema-errors is provided."
            )
    if subschema_errors is None:
        subschema_errors = "best-match"

    for filename in args_parsed.file:
        # choose source
        reader = read_from_filename
        if filename in {"-", "/-"}:
            filename = "stdin"
            reader = read_from_stdin

        # read source
        try:
            spec, base_uri = reader(filename)
        except Exception as exc:
            print(exc)
            sys.exit(1)

        # choose the validator
        validators: dict[str, type[SpecValidator] | None] = {
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
            if args_parsed.validation_errors == "all":
                if validator_cls is None:
                    validator_cls = get_validator_cls(spec)
                validator = validator_cls(spec, base_uri=base_uri)
                errors = list(validator.iter_errors())
                if errors:
                    for idx, err in enumerate(errors, start=1):
                        print_validationerror(
                            filename,
                            err,
                            subschema_errors,
                            index=idx,
                        )
                    print(f"{filename}: {len(errors)} validation errors found")
                    sys.exit(1)
                print_ok(filename)
                continue

            validate(spec, base_uri=base_uri, cls=validator_cls)
        except ValidationError as exc:
            print_validationerror(filename, exc, subschema_errors)
            sys.exit(1)
        except Exception as exc:
            print_error(filename, exc)
            sys.exit(2)
        else:
            print_ok(filename)


if __name__ == "__main__":
    main()
