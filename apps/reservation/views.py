from django.shortcuts import render
from django.db.models import Count

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from authenticate import IsTokenValid
import datetime

from apps.room.models import Kamar, NomorKamar, StatusKamar
from .models import Invoice, RoomTypeInvoice, Guest

from .serializers import KamarSerializer, RommTypeInvoiceSerializers


class ViewBook(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        date_from = request.data.get('date_from')
        date_to = request.data.get("date_to")
        tipe_kamar = request.data.get('tipe_kamar', None)
        tipe_kasur = request.data.get('tipe_kasur', None)

        dict_kamar = {
            'REGULAR': 1,
            'SUITE': 2,
            'DELUXE': 3,
            'VIP': 4,
            'FAMILY': 5
        }

        dict_kasur = {
            'TWIN': 1,
            'DOUBLE': 2,
            'QUEEN': 3,
            'KING': 4
        }
        date_from = datetime.datetime.strptime(
            date_from, "%Y-%b-%d")
        date_to = datetime.datetime.strptime(
            date_to, "%Y-%b-%d")

        status_book = StatusKamar.objects.filter(
            date_from__date=date_from,
            date_to__date=date_to,
            status_book=False
        )

        no_kamar_book = list(
            set(status_book.values_list('no_kamar__no_kamar', flat=True)))

        room = NomorKamar.objects.exclude(
            no_kamar__in=no_kamar_book, status=False)

        if tipe_kamar:
            room = room.filter(tipe_kamar__tipe_kamar=dict_kamar[tipe_kamar])

        if tipe_kasur:
            room = room.filter(tipe_kamar__tipe_kasur=dict_kasur[tipe_kasur])

        kamar = Kamar.objects.filter(id__in=room.values('tipe_kamar__id'))
        kamar = kamar.values('tipe_kamar', 'tipe_kasur', 'harga_kamar').annotate(
            total_kamar=Count('id'))

        serial = KamarSerializer(kamar, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class PesanKamar(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):

        nama = request.data.get("nama")
        email = request.data.get("email")
        nik = request.data.get('nik')
        tipe_kamar = request.data.get('tipe_kamar')
        tipe_kasur = request.data.get('tipe_kasur')
        date_from = request.data.get('date_from')
        date_to = request.data.get("date_to")
        kontak = request.data.get("kontak", None)

        date_from = datetime.datetime.strptime(
            date_from, "%Y-%b-%d")
        date_to = datetime.datetime.strptime(
            date_to, "%Y-%b-%d")

        dict_kamar = {
            'REGULAR': 1,
            'SUITE': 2,
            'DELUXE': 3,
            'VIP': 4,
            'FAMILY': 5
        }

        dict_kasur = {
            'TWIN': 1,
            'DOUBLE': 2,
            'QUEEN': 3,
            'KING': 4
        }

        obj_inv = Invoice.objects.all()
        if len(obj_inv) == 0:
            num_invoice = str(1)
        else:
            num_invoice = str(int(obj_inv.last().no_invoice) + 1)

        now = datetime.datetime.now()

        try:
            obj_guest = Guest.objects.get(nip=nik)
        except:
            Guest.objects.create(nama=nama, nip=nik,
                                 kontak=kontak, email=email)
            obj_guest = Guest.objects.get(nip=nik)
        try:
            Invoice.objects.create(no_invoice=num_invoice, guest=obj_guest,
                                   tamggal_pesan=now, tanggal_checkin=date_from, tanggal_checkout=date_to)
            obj_inv_2 = Invoice.objects.get(no_invoice=num_invoice)
        except Exception as e:
            return Response({"msg": str(e)})

        obj_room = Kamar.objects.get(
            tipe_kamar=dict_kamar[tipe_kamar], tipe_kasur=dict_kasur[tipe_kasur])

        try:
            harga = (date_to.day-date_from.day) * obj_room.harga_kamar
            RoomTypeInvoice.objects.create(
                harga=harga, invoice=obj_inv_2, room_type=obj_room)
        except Exception as e:
            return Response({"msg": str(e)})

        obj_status_kamar = StatusKamar.objects.filter(
            date_from__gte=date_from, date_to__lte=date_to, status_book=True)
        obj_nomor_kamar = NomorKamar.objects.filter(status=True, tipe_kamar__tipe_kamar=dict_kamar[tipe_kamar], tipe_kamar__tipe_kasur=dict_kasur[tipe_kasur]).exclude(
            id__in=obj_status_kamar.values('no_kamar__id')).last()
        NomorKamar.objects.filter(id=obj_nomor_kamar.id).update(status=False)

        try:
            StatusKamar.objects.create(
                date_from=date_from, date_to=date_to, status_book=True, no_kamar=obj_nomor_kamar)
        except Exception as e:
            return Response({"msg": str(e)})

        respon = {
            'kode_booking': num_invoice,
            'atas_nama': nama,
            'tanggal_pesan': now.strftime("%d-%m-%Y"),
            'tanggal_chek_in': date_from.strftime("%d-%m-%Y"),
            'tanggal_chek_out': date_to.strftime("%d-%m-%Y"),
            'tipe_kamar': tipe_kamar,
            'tipe_kasur': tipe_kasur,
            'lama_inap': date_to.day-date_from.day,
            'harga_kamar': obj_room.harga_kamar,
            'total_harga': harga,
            "msg": "Sukses memesan"
        }

        return Response(respon, status=status.HTTP_200_OK)


class CekKodeBookingGuest(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        code = request.data.get('code_booking', None)

        query = RoomTypeInvoice.objects.filter(invoice__no_invoice=code)
        serial = RommTypeInvoiceSerializers(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class UpdateCodeBookingGuest(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        code_booking = request.data.get("code_booking")
        tipe_kamar = request.data.get('tipe_kamar', None)
        tipe_kasur = request.data.get('tipe_kasur', None)
        date_from = request.data.get('date_from', None)
        date_to = request.data.get("date_to", None)

        dict_kamar = {
            'REGULAR': 1,
            'SUITE': 2,
            'DELUXE': 3,
            'VIP': 4,
            'FAMILY': 5
        }

        dict_kasur = {
            'TWIN': 1,
            'DOUBLE': 2,
            'QUEEN': 3,
            'KING': 4
        }

        try:
            query = RoomTypeInvoice.objects.get(
                invoice__no_invoice=code_booking)
        except Exception as e:
            return Response({"message": "Code Booking tida ada"}, status=status.HTTP_404_NOT_FOUND)

        date_from_old = query.invoice.tanggal_checkin
        date_to_old = query.invoice.tanggal_checkout
        obj_invoice_lama = Invoice.objects.get(id=query.invoice.id).id
        id_guest_lama = query.invoice.guest.id
        last_code_invoice = Invoice.objects.all().last().no_invoice
        harga_lama = query.room_type.harga_kamar
        tipe_kamar_old = query.room_type.tipe_kamar
        tipe_kasur_old = query.room_type.tipe_kasur

        obj_guest = Guest.objects.get(id=id_guest_lama)
        obj_nomor_kamar_old = NomorKamar.objects.filter(
            status=False, tipe_kamar__tipe_kamar=tipe_kamar_old, tipe_kamar__tipe_kasur=tipe_kasur_old).last().id
        NomorKamar.objects.filter(id=obj_nomor_kamar_old).update(status=True)
        StatusKamar.objects.filter(
            date_from=date_from_old, date_to=date_to_old, no_kamar__id=obj_nomor_kamar_old).update(status_book=False)

        if date_from:
            date_from_old = datetime.datetime.strptime(
                date_from, "%Y-%b-%d")

        if date_to:
            date_to_old = datetime.datetime.strptime(
                date_to, "%Y-%b-%d")

        if date_from and date_to:
            delta_waktu = date_to_old.day - date_from_old.day

        if tipe_kamar:
            tipe_kamar_old = dict_kamar[tipe_kamar]

        if tipe_kasur:
            tipe_kasur_old = dict_kasur[tipe_kasur]

        obj_kamar = Kamar.objects.get(
            tipe_kamar=tipe_kamar_old, tipe_kasur=tipe_kasur_old)
        harga_baru = delta_waktu*obj_kamar.harga_kamar

        if harga_baru != harga_lama:
            harga_lama = harga_baru

        num_invoice = str(int(last_code_invoice) + 1)
        now = datetime.datetime.now()

        try:
            Invoice.objects.create(no_invoice=num_invoice, guest=obj_guest,
                                   tamggal_pesan=now, tanggal_checkin=date_from_old, tanggal_checkout=date_to_old)
            obj_inv_2 = Invoice.objects.get(no_invoice=num_invoice)
            Invoice.objects.filter(id=obj_invoice_lama).update(status=False)
        except Exception as e:
            return Response({"msg": str(e)})

        try:
            RoomTypeInvoice.objects.filter(invoice__id=obj_invoice_lama).update(
                harga=harga_lama, invoice=obj_inv_2, room_type=obj_kamar)
        except Exception as e:
            return Response({"msg": str(e)})

        obj_status_kamar = StatusKamar.objects.filter(
            date_from__gte=date_from_old, date_to__lte=date_to_old, status_book=True)
        obj_nomor_kamar = NomorKamar.objects.filter(status=True, tipe_kamar__tipe_kamar=tipe_kamar_old, tipe_kamar__tipe_kasur=tipe_kasur_old).exclude(
            id__in=obj_status_kamar.values('no_kamar__id')).last()
        NomorKamar.objects.filter(id=obj_nomor_kamar.id).update(status=False)

        try:
            StatusKamar.objects.create(
                date_from=date_from_old, date_to=date_to_old, status_book=True, no_kamar=obj_nomor_kamar)
        except Exception as e:
            return Response({"msg": str(e)})

        respon = {
            'kode_booking': num_invoice,
            'tanggal_pesan': now.strftime("%d-%m-%Y"),
            'tanggal_chek_in': date_from_old.strftime("%d-%m-%Y"),
            'tanggal_chek_out': date_to_old.strftime("%d-%m-%Y"),
            'tipe_kamar': tipe_kamar_old,
            'tipe_kasur': tipe_kasur_old,
            'lama_inap': date_to_old.day-date_from_old.day,
            'harga_kamar': obj_kamar.harga_kamar,
            'total_harga': harga_lama,
            "msg": "Sukses merubah pesanan memesan"
        }

        return Response(respon, status=status.HTTP_200_OK)


class DeleteCodeBook(APIView):
    permission_classes = (IsTokenValid,)

    def post(self, request):

        code_booking = request.data.get("code_booking")
        try:
            obj_in = RoomTypeInvoice.objects.get(
                invoice__no_invoice=code_booking)
            obj_status_kamar = StatusKamar.objects.filter(date_from=obj_in.invoice.tanggal_checkin, date_to=obj_in.invoice.tanggal_checkout, no_kamar__status=False,
                                                          no_kamar__tipe_kamar__tipe_kamar=obj_in.room_type.tipe_kamar, no_kamar__tipe_kamar__tipe_kasur=obj_in.room_type.tipe_kasur, status_book=True)
            id_status = obj_status_kamar.last().id
            print(id_status)
            NomorKamar.objects.filter(
                id=obj_status_kamar.last().no_kamar.id).update(status=True)
            StatusKamar.objects.filter(id=id_status).update(status_book=False)
            Invoice.objects.filter(
                no_invoice=code_booking).update(status=False)
        except Exception as e:
            return Response({"msg": str(e)})

        return Response({"msg": "data berhasil dihapus"})
