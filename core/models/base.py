import uuid
from django.db import models

class SoftDeleteTimestampModel(models.Model):
    """
    Abstract base model that maintains created/updated timestamps 
    and soft-delete state for delta-sync architecture.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
