# Generated by Django 5.0 on 2023-12-28 21:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0002_kamar_kapasitas"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nomorkamar",
            name="status",
        ),
        migrations.CreateModel(
            name="StatusKamar",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_from", models.DateTimeField()),
                ("date_to", models.DateTimeField()),
                ("status_book", models.BooleanField(default=True)),
                (
                    "no_kamar",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="room.nomorkamar",
                    ),
                ),
            ],
        ),
    ]
