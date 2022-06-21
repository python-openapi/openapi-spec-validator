FROM python:3.7-alpine

ARG OPENAPI_SPEC_VALIDATOR_VERSION=0.5.0a2

RUN pip install --no-cache-dir openapi-spec-validator==${OPENAPI_SPEC_VALIDATOR_VERSION}

ENTRYPOINT ["openapi-spec-validator"]
