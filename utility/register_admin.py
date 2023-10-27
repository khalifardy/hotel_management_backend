from django.contrib import admin
from django.apps import apps


def register_all_models(nama_aplikasi):
    app_models = apps.get_app_config(nama_aplikasi).get_models()

    for model in app_models:
        admin.site.register(model)
