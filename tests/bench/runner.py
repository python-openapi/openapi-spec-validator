#!/usr/bin/env python3
"""
Benchmark suite for openapi-spec-validator performance testing.

Usage:
    python runner.py --output results.json
    python runner.py --profile  # Generates profile data
"""

import argparse
import cProfile
import gc
import json
import pstats
import statistics
import time
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from io import StringIO
from pathlib import Path
from typing import Any

from jsonschema_path.typing import Schema

from openapi_spec_validator import schemas
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator.settings import OpenAPISpecValidatorSettings


@dataclass
class BenchResult:
    spec_name: str
    spec_version: str
    spec_size_kb: float
    paths_count: int
    schemas_count: int
    repeats: int
    warmup: int
    seconds: list[float]
    success: bool
    error: str | None = None

    @cached_property
    def median_s(self) -> float | None:
        if self.seconds:
            return statistics.median(self.seconds)
        return None

    @cached_property
    def mean_s(self) -> float | None:
        if self.seconds:
            return statistics.mean(self.seconds)
        return None

    @cached_property
    def stdev_s(self) -> float | None:
        if len(self.seconds) > 1:
            return statistics.pstdev(self.seconds)
        return None

    @cached_property
    def validations_per_sec(self) -> float | None:
        if self.median_s:
            return 1 / self.median_s
        return None

    def as_dict(self) -> dict[str, Any]:
        return {
            "spec_name": self.spec_name,
            "spec_version": self.spec_version,
            "spec_size_kb": self.spec_size_kb,
            "paths_count": self.paths_count,
            "schemas_count": self.schemas_count,
            "repeats": self.repeats,
            "warmup": self.warmup,
            "seconds": self.seconds,
            "median_s": self.median_s,
            "mean_s": self.mean_s,
            "stdev_s": self.stdev_s,
            "validations_per_sec": self.validations_per_sec,
            "success": self.success,
            "error": self.error,
        }


def count_paths(spec: Schema) -> int:
    """Count paths in OpenAPI spec."""
    return len(spec.get("paths", {}))


def count_schemas(spec: Schema) -> int:
    """Count schemas in OpenAPI spec."""
    components = spec.get("components", {})
    definitions = spec.get("definitions", {})  # OpenAPI 2.0
    return len(components.get("schemas", {})) + len(definitions)


def get_spec_version(spec: Schema) -> str:
    """Detect OpenAPI version."""
    if "openapi" in spec:
        return spec["openapi"]
    elif "swagger" in spec:
        return spec["swagger"]
    return "unknown"


def run_once(spec: Schema) -> float:
    """Run validation once and return elapsed time."""
    t0 = time.perf_counter()
    validate(spec)
    return time.perf_counter() - t0


def benchmark_spec_file(
    spec_path: Path,
    repeats: int = 7,
    warmup: int = 2,
    no_gc: bool = False,
) -> BenchResult:
    spec_name = spec_path.name
    spec_size_kb = spec_path.stat().st_size / 1024
    spec, _ = read_from_filename(str(spec_path))
    return benchmark_spec(
        spec,
        repeats,
        warmup,
        no_gc,
        spec_name=spec_name,
        spec_size_kb=spec_size_kb,
    )


def benchmark_spec(
    spec: Schema,
    repeats: int = 7,
    warmup: int = 2,
    no_gc: bool = False,
    profile: str | None = None,
    spec_name: str = "spec",
    spec_size_kb: float = 0,
) -> BenchResult:
    """Benchmark a single OpenAPI spec."""
    try:
        spec_version = get_spec_version(spec)
        paths_count = count_paths(spec)
        schemas_count = count_schemas(spec)
        print(
            f"⚡ Benchmarking {spec_name} spec (version {spec_version}, {paths_count} paths, {schemas_count} schemas)..."
        )

        if no_gc:
            gc.disable()

        # Warmup
        for _ in range(warmup):
            run_once(spec)

        pr: cProfile.Profile | None = None
        if profile:
            print("\n🔬 Profiling mode enabled...")
            pr = cProfile.Profile()
            pr.enable()

        # Actual benchmark
        seconds: list[float] = []
        for _ in range(repeats):
            seconds.append(run_once(spec))

        if profile:
            assert pr is not None
            pr.disable()

            # Print profile stats
            s = StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
            ps.print_stats(30)
            print(s.getvalue())

            # Save profile data
            pr.dump_stats(profile)
            print(f"💾 Profile data saved to {profile}")
            print(f"   View with: python -m pstats {profile}")

        if no_gc:
            gc.enable()

        return BenchResult(
            spec_name=spec_name,
            spec_version=spec_version,
            spec_size_kb=spec_size_kb,
            paths_count=paths_count,
            schemas_count=schemas_count,
            repeats=repeats,
            warmup=warmup,
            seconds=seconds,
            success=True,
        )

    except Exception as e:
        return BenchResult(
            spec_name=spec_name,
            spec_version="unknown",
            spec_size_kb=spec_size_kb,
            paths_count=0,
            schemas_count=0,
            repeats=repeats,
            warmup=warmup,
            seconds=[],
            success=False,
            error=str(e),
        )


def generate_synthetic_spec(
    paths: int,
    schemas: int,
    version: str = "3.0.0",
) -> dict[str, Any]:
    """Generate synthetic OpenAPI spec for stress testing."""
    paths_obj = {}
    for i in range(paths):
        paths_obj[f"/resource/{i}"] = {
            "get": {
                "responses": {
                    "200": {
                        "description": "Success",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f"#/components/schemas/Schema{i % schemas}"
                                }
                            }
                        },
                    }
                }
            }
        }

    schemas_obj = {}
    for i in range(schemas):
        schemas_obj[f"Schema{i}"] = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "nested": {
                    "$ref": f"#/components/schemas/Schema{(i + 1) % schemas}"
                },
            },
        }

    return {
        "openapi": version,
        "info": {
            "title": f"Synthetic API ({paths} paths, {schemas} schemas)",
            "version": "1.0.0",
        },
        "paths": paths_obj,
        "components": {"schemas": schemas_obj},
    }


def get_synthetic_specs_iterator(
    configs: list[tuple[int, int, str]],
) -> Iterator[tuple[dict[str, Any], str, float]]:
    """Iterator over synthetic specs based on provided configurations."""
    for paths, schema_count, size in configs:
        spec = generate_synthetic_spec(paths, schema_count)
        yield spec, f"synthetic_{size}", 0


def get_specs_iterator(
    spec_files: list[Path],
) -> Iterator[tuple[Schema, str, float]]:
    """Iterator over provided spec files."""
    for spec_file in spec_files:
        spec, _ = read_from_filename(str(spec_file))
        yield spec, spec_file.name, spec_file.stat().st_size / 1024


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark openapi-spec-validator"
    )
    parser.add_argument(
        "specs",
        type=Path,
        nargs="*",
        help="File(s) with custom specs to benchmark, otherwise use synthetic specs.",
    )
    parser.add_argument(
        "--repeats", type=int, default=1, help="Number of benchmark repeats"
    )
    parser.add_argument(
        "--warmup", type=int, default=0, help="Number of warmup runs"
    )
    parser.add_argument(
        "--no-gc", action="store_true", help="Disable GC during benchmark"
    )
    parser.add_argument("--output", type=str, help="Output JSON file path")
    parser.add_argument(
        "--profile", type=str, help="Profile file path (cProfile)"
    )
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    settings = OpenAPISpecValidatorSettings()

    print("Spec schema validator backend selection:")
    print("  Configured backend mode: " f"{settings.schema_validator_backend}")
    print(f"  Effective backend: {schemas.get_validator_backend()}")

    # Benchmark custom specs
    if args.specs:
        print(
            f"\n🔍 Testing with custom specs {[str(spec) for spec in args.specs]}"
        )
        spec_iterator = get_specs_iterator(args.specs)

    # Synthetic specs for stress testing
    else:
        print("\n🔍 Testing with synthetic specs")
        synthetic_configs = [
            (10, 5, "small"),
            (50, 20, "medium"),
            (200, 100, "large"),
            (500, 250, "xlarge"),
        ]
        spec_iterator = get_synthetic_specs_iterator(synthetic_configs)

    # Iterate over provided specs
    for spec, spec_name, spec_size_kb in spec_iterator:
        result = benchmark_spec(
            spec,
            repeats=args.repeats,
            warmup=args.warmup,
            no_gc=args.no_gc,
            profile=args.profile,
            spec_name=spec_name,
            spec_size_kb=spec_size_kb,
        )
        results.append(result.as_dict())
        if result.success:
            print(
                "   ✅ {:.4f}s, {:.2f} val/s".format(
                    result.median_s,
                    result.validations_per_sec,
                )
            )
        else:
            print(f"   ❌ Error: {result.error}")

    # Output results
    output = {
        "benchmark_config": {
            "repeats": args.repeats,
            "warmup": args.warmup,
            "no_gc": args.no_gc,
        },
        "results": results,
    }

    print(f"\n📊 Summary: {len(results)} specs benchmarked")
    print(json.dumps(output, indent=2))

    if args.output:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")


if __name__ == "__main__":
    main()
