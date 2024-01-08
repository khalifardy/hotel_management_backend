from rest_framework import serializers
from .models import Invoice, RoomTypeInvoice, Guest
from apps.room.models import Kamar


class KamarSerializer(serializers.Serializer):

    dict_kamar = {
        1: 'REGULAR',
        2: 'SUITE',
        3: 'DELUXE',
        4: 'VIP',
        5: 'FAMILY'
    }

    dict_kasur = {
        1: 'TWIN',
        2: 'DOUBLE',
        3: 'QUEEN',
        4: 'KING'
    }
    tipe_kamar = serializers.CharField()
    tipe_kasur = serializers.CharField()
    total_kamar = serializers.IntegerField()
    harga_kamar = serializers.DecimalField(max_digits=65, decimal_places=2)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tipe_kamar'] = self.dict_kamar.get(
            instance['tipe_kamar'], instance['tipe_kamar'])
        representation['tipe_kasur'] = self.dict_kasur.get(
            instance['tipe_kasur'], instance['tipe_kasur'])
        return representation


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['nama', 'nip', 'kontak', 'email']


class InvoiceSerializer(serializers.ModelSerializer):

    guest = GuestSerializer()
    tamggal_pesan = serializers.SerializerMethodField()
    tanggal_checkin = serializers.SerializerMethodField()
    tanggal_checkout = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['no_invoice', 'guest', 'tamggal_pesan',
                  'tanggal_checkin', 'tanggal_checkout']

    def get_tamggal_pesan(self, obj):
        print(obj)
        return obj.tamggal_pesan.strftime("%d-%m-%Y")

    def get_tanggal_checkin(self, obj):
        return obj.tanggal_checkin.strftime("%d-%m-%Y")

    def get_tanggal_checkout(self, obj):
        return obj.tanggal_checkout.strftime("%d-%m-%Y")


class KamarSerializer2(serializers.ModelSerializer):
    dict_kamar = {
        1: 'REGULAR',
        2: 'SUITE',
        3: 'DELUXE',
        4: 'VIP',
        5: 'FAMILY'
    }

    dict_kasur = {
        1: 'TWIN',
        2: 'DOUBLE',
        3: 'QUEEN',
        4: 'KING'
    }
    tipe_kamar = serializers.SerializerMethodField()
    tipe_kasur = serializers.SerializerMethodField()

    class Meta:
        model = Kamar
        fields = ['tipe_kamar', 'tipe_kasur', 'harga_kamar']

    def get_tipe_kamar(self, obj):
        return self.dict_kamar[obj.tipe_kamar]

    def get_tipe_kasur(self, obj):
        return self.dict_kasur[obj.tipe_kasur]


class RommTypeInvoiceSerializers(serializers.ModelSerializer):

    invoice = InvoiceSerializer()
    room_type = KamarSerializer2()

    class Meta:
        model = RoomTypeInvoice
        fields = ['invoice', 'room_type', 'harga']
