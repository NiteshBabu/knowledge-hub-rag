from app.core.celery import celery_app
from app.services.document_processing import DocumentProcessingService


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_document_task(
    self,
    document_id: int,
    file_path: str,
):
    DocumentProcessingService.process_document(
        document_id=document_id,
        file_path=file_path,
    )
