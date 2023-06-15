ARG OPENAPI_SPEC_VALIDATOR_VERSION=0.6.0a1

FROM python:3.11.4-alpine as builder

ARG OPENAPI_SPEC_VALIDATOR_VERSION

ENV CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse

RUN apk add --no-cache cargo
RUN python -m pip wheel --wheel-dir /wheels openapi-spec-validator==${OPENAPI_SPEC_VALIDATOR_VERSION}

FROM python:3.11.4-alpine

ARG OPENAPI_SPEC_VALIDATOR_VERSION

COPY --from=builder /wheels /wheels
RUN apk add --no-cache libgcc
RUN pip install --no-cache-dir --pre --find-links /wheels openapi-spec-validator==${OPENAPI_SPEC_VALIDATOR_VERSION} && \
    rm -r /wheels

ENTRYPOINT ["openapi-spec-validator"]
