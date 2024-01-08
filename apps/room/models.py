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
    kapasitas = models.IntegerField(null=True, blank=True)
    harga_kamar = models.DecimalField(max_digits=65, decimal_places=2)

    class Meta:
        app_label = "room"
        verbose_name = "kamar"
        verbose_name_plural = "kamar"


class NomorKamar(models.Model):

    no_kamar = models.IntegerField(blank=True, null=True)
    tipe_kamar = models.ForeignKey(Kamar, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        app_label = "room"
        verbose_name = "Nomorkamar"
        verbose_name_plural = "Nomorkamar"

    def __str__(self):
        return str(self.no_kamar)


class StatusKamar(models.Model):

    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    status_book = models.BooleanField(default=True)
    no_kamar = models.ForeignKey(NomorKamar, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.no_kamar.no_kamar)
