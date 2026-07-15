FROM python:3.12-slim

WORKDIR /app

COPY backend/ .

RUN pip install -r requirements.txt

RUN chmod +x start.sh

# CMD ["celery", "-A", "app.core.celery:celery_app", "worker", "--loglevel=info"]

CMD ["./start.sh"]