# Generated by Django 4.2.3 on 2023-10-27 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0002_kamar_kapasitas"),
        ("services", "0003_remove_pesan_jumlah_pesanan_remove_pesan_pesanan_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pesan",
            name="guest",
        ),
        migrations.AddField(
            model_name="pesan",
            name="atas_nama",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="pesan",
            name="no_kamar",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="room.nomorkamar"
            ),
        ),
    ]