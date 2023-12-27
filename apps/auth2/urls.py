from django.urls import re_path
from .views import Login, SignupStaff

urlpatterns = [
    re_path(r'^login/$', Login.as_view(), name='Login'),
    re_path(r'^signup/staff/$', SignupStaff.as_view(), name='Login')
]
