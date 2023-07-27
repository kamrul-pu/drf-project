"""Choices for core app."""

from django.db import models


class UserKind(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    STUDENT = "STUDENT", "Student"
    TEACHER = "TEACHER", "Teacher"
    UNDEFINED = "UNDEFINED", "Undefined"


class UserStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    DRAFT = "DRAFT", "Draft"
    INACTIVE = "INACTIVE", "Inactive"
