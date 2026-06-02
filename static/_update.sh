#!/bin/bash

# check:
#    https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/#self-hosting-javascript-and-css-for-docs

STATIC_FILES+="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js "
STATIC_FILES+="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css "
STATIC_FILES+="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js "

STATIC_DIR="$(dirname "$(realpath "${0}")")"

for STATIC_FILE in ${STATIC_FILES}; do
  curl -o "${STATIC_DIR}/$(basename "${STATIC_FILE}")" "${STATIC_FILE}"
done
