from django.urls import re_path
from .views import Login, SignupStaff, Signup, LogoutView

urlpatterns = [
    re_path(r'^login/$', Login.as_view(), name='Login'),
    re_path(r'^signup/staff/$', SignupStaff.as_view(), name='SignUpStaff'),
    re_path(r'^signup/$', Signup.as_view(), name='Signup'),
    re_path(r'^logout/$', LogoutView.as_view(), name='Logout')
]
