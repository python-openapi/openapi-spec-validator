ARG OPENAPI_SPEC_VALIDATOR_VERSION=0.9.0

FROM python:3.14.5-alpine as builder

ARG OPENAPI_SPEC_VALIDATOR_VERSION

ENV CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse

RUN apk add --no-cache cargo
RUN python -m pip wheel --wheel-dir /wheels openapi-spec-validator==${OPENAPI_SPEC_VALIDATOR_VERSION}

FROM python:3.14.5-alpine

ARG OPENAPI_SPEC_VALIDATOR_VERSION

RUN apk add --no-cache libgcc
RUN --mount=type=bind,from=builder,source=/wheels,target=/wheels \
    pip install --no-cache-dir --pre --find-links /wheels openapi-spec-validator==${OPENAPI_SPEC_VALIDATOR_VERSION}

ENTRYPOINT ["openapi-spec-validator"]
