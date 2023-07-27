"""Models for our Watchlist app."""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from common.choices import Status
from common.managers import CustomManager
from common.models import BaseModelWithUUID


User = get_user_model()


class StreamPlatform(BaseModelWithUUID):
    name = models.CharField(
        max_length=30,
        db_index=True,
    )
    about = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    website = models.URLField()
    objects = CustomManager()

    def __str__(self) -> str:
        return self.name


class WatchList(BaseModelWithUUID):
    title = models.CharField(
        max_length=50,
        db_index=True,
    )
    story_line = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    platform = models.ForeignKey(
        StreamPlatform,
        on_delete=models.CASCADE,
        related_name="watchlist",
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    avg_rating = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        default=0.0,
    )
    number_of_rating = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at",)


class Review(BaseModelWithUUID):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    watchlist = models.ForeignKey(
        WatchList,
        on_delete=models.CASCADE,
        related_name="watchlist_review",
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.rating}"

    class Meta:
        ordering = ("-created_at",)
