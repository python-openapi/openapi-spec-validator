FROM python:3.11-alpine

ARG OPENAPI_SPEC_VALIDATOR_VERSION=0.6.0a1

RUN pip install --no-cache-dir --pre openapi-spec-validator==${OPENAPI_SPEC_VALIDATOR_VERSION}

ENTRYPOINT ["openapi-spec-validator"]
