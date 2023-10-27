from django.contrib import admin
# Register your models here.
from utility.register_admin import register_all_models

register_all_models("services")
