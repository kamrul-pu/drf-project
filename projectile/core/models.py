"""Core models for our app."""

import uuid

from django.db import models
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from core.choices import UserKind, UserStatus


class UserManager(BaseUserManager):
    """Managers for users."""

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("User must have a phone number")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        """Create a new superuser and return superuser"""
        user = self.create_user(phone=phone, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    kind = models.CharField(
        max_length=50,
        choices=UserKind.choices,
        default=UserKind.UNDEFINED,
    )
    status = models.CharField(
        max_length=50,
        choices=UserStatus.choices,
        default=UserStatus.DRAFT,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"

    class Meta:
        verbose_name = "System User"
        verbose_name_plural = "System Users"
