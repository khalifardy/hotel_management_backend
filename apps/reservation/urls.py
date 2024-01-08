from django.urls import re_path
from .views import ViewBook, PesanKamar, CekKodeBookingGuest, UpdateCodeBookingGuest, DeleteCodeBook

urlpatterns = [
    re_path(r'^viewroom/$', ViewBook.as_view(), name='view'),
    re_path(r'^pesankamar/$', PesanKamar.as_view(), name='pesan'),
    re_path(r'^cekkodebooking/guest/$',
            CekKodeBookingGuest.as_view(), name='cek'),
    re_path(r'^updatekodebooking/guest/$',
            UpdateCodeBookingGuest.as_view(), name='update'),
    re_path(r'^deletekodebooking/guest/$',
            DeleteCodeBook.as_view(), name='delete'),
]
