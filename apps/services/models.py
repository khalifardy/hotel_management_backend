from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.reservation.models import Invoice, Guest
from apps.room.models import NomorKamar
# Create your models here.


class CICO(TimeStampedModel):
    guest = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date_check_in = models.DateTimeField(null=True, blank=True)
    date_check_out = models.DateTimeField(null=True, blank=True)
    no_kamar = models.ForeignKey(NomorKamar, on_delete=models.CASCADE)
    status_ci = models.BooleanField(default=False)
    status_co = models.BooleanField(default=False)


class Menu(models.Model):

    menu = models.CharField(max_length=500)
    kategori = models.CharField(max_length=500)
    harga_satuan = models.DecimalField(max_digits=65, decimal_places=2)

    def __str__(self):
        return self.menu


class Pesan(TimeStampedModel):
    WAITING_LIST = 1
    COOKING = 2
    DELIVERED = 3

    STATUS = [
        (WAITING_LIST, "Waiting List"),
        (COOKING, "Cooking"),
        (DELIVERED, "Delivered")
    ]
    atas_nama = models.CharField(max_length=500, null=True, blank=True)
    no_kamar = models.ForeignKey(NomorKamar, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=WAITING_LIST)


class CatatanPesanan(models.Model):
    guest = models.ForeignKey(Pesan, on_delete=models.CASCADE)
    pesanan = models.ForeignKey(Menu, on_delete=models.CASCADE)
    jumlah_pesanan = models.IntegerField()
    total_harga = models.DecimalField(max_digits=65, decimal_places=2)
