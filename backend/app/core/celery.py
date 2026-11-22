import ssl

from app.core.settings import settings
from celery import Celery

celery_app = Celery(
    "knowledgehub",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.documents"],
)

celery_app.conf.task_track_started = True

celery_app.conf.broker_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}
celery_app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

celery_app.autodiscover_tasks(["app"])
