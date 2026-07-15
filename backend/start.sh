#!/bin/sh

celery -A app.core.celery.celery_app worker -l info &
exec uvicorn app.api.main:app --host 0.0.0.0 --port "${PORT:-8000}"