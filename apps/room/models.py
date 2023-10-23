from django.db import models

# Create your models here.


class Kamar(models.Model):
    REGULAR = 1
    SUITE = 2
    DELUXE = 3
    VIP = 4
    FAMILY = 5

    ROOM = [
        (REGULAR, "regular"),
        (SUITE, "suite"),
        (DELUXE, "deluxe"),
        (VIP, "VIP"),
        (FAMILY, "Family")
    ]

    TWIN = 1
    DOUBLE = 2
    QUEEN = 3
    KING = 4

    BED = [
        (TWIN, "Twin bed"),
        (DOUBLE, "Double bed"),
        (QUEEN, "Queen bed"),
        (KING, "King bed")
    ]

    tipe_kamar = models.IntegerField(
        choices=ROOM, default=REGULAR, blank=True, null=True
    )

    tipe_kasur = models.IntegerField(
        choices=BED, default=TWIN, blank=True, null=True
    )
    harga_kamar = models.DecimalField(max_digits=65, decimal_places=2)

    class Meta:
        app_label = "room"
        verbose_name = "kamar"
        verbose_name_plural = "kamar"


class NomorKamar(models.Model):

    no_kamar = models.IntegerField(blank=True, null=True)
    tipe_kamar = models.ForeignKey(Kamar, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        app_label = "room"
        verbose_name = "Nomorkamar"
        verbose_name_plural = "Nomorkamar"
