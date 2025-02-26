from rest_framework import serializers
from registration.models import Packing, Extradition
from users.models import Client
from django.db.models import Sum


class PackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packing
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):
    total_stock = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'company_name', 'total_stock')  # Включаем total_stock

    def get_total_stock(self, obj):
        # Получаем суммарный баланс для текущего клиента
        return Extradition.objects.filter(client=obj).aggregate(
            total_stock=Sum('balance_storage'))['total_stock'] or 0


class ExtraditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extradition
        fields = ['id', 'balance_storage', 'created_at']


class ClientSerializer(serializers.ModelSerializer):
    extradition_list = serializers.SerializerMethodField()
    extradition_details = ExtraditionSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

    def get_extradition_list(self, obj):
        extraditions = Extradition.objects.filter(client=obj, balance_storage__gt=0)
        if extraditions.exists():
            return ExtraditionSerializer(extraditions, many=True).data
        return {"message": "Задолженностей не найдено"}
