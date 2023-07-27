"""Common Choices"""
from django.db.models import TextChoices


class Status(TextChoices):
    ACTIVE = "ACTIVE", "Active"
    ARCHIVED = "ARCHIVED", "ARCHIVED"
    DRAFT = "DRAFT", "Draft"
    DELETED = "DELETED", "Deleted"
