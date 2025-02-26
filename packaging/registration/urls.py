from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path(  # Home
        '',
        views.registration_view,
        name='index'
    ),
    path(
        'clients/',
        views.clients_table,
        name='clients'
    ),
    path(
        'packing/',
        views.packing_table,
        name='packing'
    ),
    path(
        'client/<int:client_id>/',
        views.client_view,
        name='client'
    ),
    path(
        'historyclient/<int:client_id>/',
        views.history_table_client,
        name='historyclient'
    ),
    path(
        'report/',
        views.report_table,
        name='report'
    ),
    path(
        'reportclient/<int:client_id>/',
        views.report_table_client,
        name='reportclient'
    ),
    path(
        'reportpacking/<int:packing_id>/',
        views.report_table_packing,
        name='reportpacking'
    ),
    path(
        'reportpacking/<int:year>-<int:month>-<int:day>/',
        views.report_table_date,
        name='reportdate'
    ),
]
