from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ClientDetailView, PackingViewSet, ClientsViewSet, ExtraditionListView
)

router = DefaultRouter()
router.register(r'packing', PackingViewSet)
router.register(r'clients', ClientsViewSet)

urlpatterns = [
    path('client/<int:client_id>/', ClientDetailView.as_view(), name='client-detail'),
    # path('extradition/', ExtraditionListView.as_view(), name='extradition-list'),
    path('', include(router.urls)),
]
