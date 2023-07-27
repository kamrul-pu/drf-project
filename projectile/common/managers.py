from django.db import models
from common.choices import Status


class CustomManager(models.Manager):
    def get_all_actives(self):
        return self.get_queryset().filter(
            status=Status.ACTIVE,
        )
