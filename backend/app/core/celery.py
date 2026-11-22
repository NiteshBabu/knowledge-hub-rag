import ssl

from app.core.settings import settings
from celery import Celery

celery_app = Celery(
    "knowledgehub",
    broker=settings.redis_url,
    backend=settings.redis_url,
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_ignore_result=True,
    include=["app.tasks.documents"],
)

celery_app.conf.task_track_started = True

celery_app.conf.broker_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}
celery_app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

celery_app.autodiscover_tasks(["app"])
