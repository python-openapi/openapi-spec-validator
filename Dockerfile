FROM python:3.11-alpine

ARG OPENAPI_SPEC_VALIDATOR_VERSION=0.5.7

RUN pip install --no-cache-dir openapi-spec-validator==${OPENAPI_SPEC_VALIDATOR_VERSION}

ENTRYPOINT ["openapi-spec-validator"]
