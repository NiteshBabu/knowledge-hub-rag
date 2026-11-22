#!/bin/bash
set -e

celery -A app.core.celery.celery_app worker \
    --loglevel=warning \
    --concurrency=1 \
    --pool=solo &

exec uvicorn app.api.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --workers 1