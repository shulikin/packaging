from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Client
from registration.models import Packing, Extradition
from api.serializers import (
    PackingSerializer,
    ClientsSerializer,
    ClientSerializer,
    ExtraditionSerializer
)


class ClientDetailView(APIView):
    def get(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response(
                {"error": "Client not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class PackingViewSet(viewsets.ModelViewSet):
    queryset = Packing.objects.all()
    serializer_class = PackingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientsSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ExtraditionListView(ListAPIView):
    serializer_class = ExtraditionSerializer

    def get_queryset(self):
        client_id = self.request.query_params.get('client_id')
        if not client_id:
            return Extradition.objects.none()
        return Extradition.objects.filter(
            client_id=client_id,
            balance_storage__gt=0
        )
