from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

# Create your models here.


class Guest(TimeStampedModel):
    nama = models.CharField(max_length=500, default="")
    nip = models.CharField(max_length=500, default="")

    kontak = models.CharField(
        max_length=100, default="", blank=True, null=True)
    email = models.CharField(max_length=100, default="", blank=True, null=True)
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        app_label = "reservation"
        verbose_name = "guest"
        verbose_name_plural = "guest"
