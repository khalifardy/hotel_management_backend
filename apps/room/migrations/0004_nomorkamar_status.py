# Generated by Django 5.0 on 2023-12-28 22:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0003_remove_nomorkamar_status_statuskamar"),
    ]

    operations = [
        migrations.AddField(
            model_name="nomorkamar",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]