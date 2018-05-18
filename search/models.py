from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User


class ExtractQuery(models.Model):
    query_params = JSONField()

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    name = models.CharField(
        max_length=256, blank=True, default=""
    )

    def to_dict(self, user):
        return self.query_params
