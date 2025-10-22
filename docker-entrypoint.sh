#!/bin/bash
###############################################################################

alembic upgrade head
uvicorn "${UVICORN_APP}" --host "${UVICORN_HOST}" --port "${UVICORN_PORT}" --proxy-headers --reload
