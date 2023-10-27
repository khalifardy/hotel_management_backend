from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from apps.room.models import Kamar

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


class Invoice(TimeStampedModel):
    no_invoice = models.CharField(max_length=500, null=True, blank=True)
    guest = models.ForeignKey(
        Guest, null=True, blank=True, on_delete=models.CASCADE)
    tamggal_pesan = models.DateTimeField(blank=True, null=True)
    tanggal_checkin = models.DateTimeField(blank=True, null=True)
    tanggal_checkout = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.no_invoice


class RoomTypeInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    room_type = models.ForeignKey(
        Kamar, null=True, blank=True, on_delete=models.CASCADE)
    harga = models.DecimalField(decimal_places=2, max_digits=65, default=0)
