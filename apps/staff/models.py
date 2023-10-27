from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class Role(models.Model):
    MANAGEMENT = 1
    RESEPSIONIS = 2
    ROOM_SERVICE = 3
    CHEF = 4
    SECURITY = 5

    LEVELS = [
        (MANAGEMENT, "management"),
        (RESEPSIONIS, "resepsionis"),
        (ROOM_SERVICE, "Room Services"),
        (CHEF, "Chef"),
        (SECURITY, "Security"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipe = models.IntegerField(
        choices=LEVELS, default=RESEPSIONIS, blank=True, null=True
    )

    class Meta:
        app_label = "staff"
        verbose_name = "Level"
        verbose_name_plural = "Level"


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE
    )
    full_name = models.CharField(blank=True, null=True, max_length=100)
    nik = models.CharField(blank=True, null=True, max_length=100)
    email = models.CharField(blank=True, null=True, max_length=100)
    kontak = models.CharField(blank=True, null=True, max_length=100)
    contract_date = models.DateTimeField(blank=True, null=True)
    bod = models.DateTimeField(blank=True, null=True)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
