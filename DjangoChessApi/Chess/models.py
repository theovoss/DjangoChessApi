from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL


class GameType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    rules = JSONField()
    created_by = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
