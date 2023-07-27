"""Common models for all app."""
from uuid import uuid4
from django.db import models

from common.choices import Status


class BaseModelWithUUID(models.Model):
    uid = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    status = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        abstract = True
