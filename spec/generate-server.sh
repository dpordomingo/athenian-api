#!/bin/sh
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/spec/openapi.yaml -g python-aiohttp -o /local/server --git-repo-id athenianco/athenian-api --package-name athenian.api
black server
