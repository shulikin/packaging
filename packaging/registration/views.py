from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum

from users.models import Client
from .models import (
    Packing,
    Extradition,
    Comeback,
    Register
)
from .forms import (
    FormExtradition,
    ComebackForm,
    PackingForm
)
ELEMENT_PAGE = 10


@login_required
def registration_view(request):
    """Отображает страницу регистрации."""

    return render(request, 'registration/registration.html')


def paginate_queryset(queryset, request, items_per_page=ELEMENT_PAGE):
    """Пагинирует переданный queryset."""

    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@login_required
def clients_table(request):
    """Отображает таблицу клиентов."""

    table = Client.objects.annotate(
        total_stock=Sum('extradition__balance_storage')
    )
    client_data = [
        {
            'client': client,
            'total_stock': client.total_stock or 0
        }
        for client in table
    ]
    page_obj = paginate_queryset(client_data, request, ELEMENT_PAGE)

    if request.method == 'POST':
        form_extradition = FormExtradition(request.POST)
        if form_extradition.is_valid():
            data = form_extradition.cleaned_data
            packing = Packing.objects.get(id=data['packing'].id)
            if packing.balance - data['amount'] < 0:
                form_extradition.add_error(
                    None,
                    'Нельзя отгрузить тару '
                    'которой нет на складе!'
                )
            else:
                extradition = form_extradition.save(commit=False)
                extradition.balance_storage = data['amount']
                extradition.user = request.user
                packing.balance -= data['amount']
                packing.save()
                extradition.save()
                return redirect('registration:clients')
    else:
        form_extradition = FormExtradition()

    context = {
        'button_class': 'btn btn-success btn-sm',
        'form_extradition': form_extradition,
        'page_obj': page_obj,
    }
    return render(request, 'registration/clients.html', context)


@login_required
def client_view(request, client_id):
    """Информация о клиенте и манипуляции с тарой."""

    client = get_object_or_404(Client, pk=client_id)
    table = Extradition.objects.filter(
        client_id=client_id,
        balance_storage__gt=0
    )
    page_obj = paginate_queryset(table, request, ELEMENT_PAGE)

    if request.method == 'POST':
        form = ComebackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            extradition = Extradition.objects.get(id=data['extradition_id'])
            if extradition.balance_storage - data['balance_amount'] < 0:
                form.add_error(
                    None,
                    'Количество возвращаемой тары '
                    'не может быть больше клиентского долга!'
                )
            else:
                Comeback.objects.create(
                    amount=data['balance_amount'],
                    text=data['text'],
                    client_id=data['client_id'],
                    packing_id=data['packing_id'],
                    user=request.user
                )
                extradition.balance_storage -= data['balance_amount']
                extradition.save()
                packing = Packing.objects.get(id=data['packing_id'])
                packing.balance += data['balance_amount']
                packing.save()
                return redirect('registration:client', client_id=client_id)
    else:
        form = ComebackForm()

    context = {
        'button_class': 'btn btn-success btn-sm',
        'client': client,
        'page_obj': page_obj,
        'form': form
    }
    return render(request, 'registration/client.html', context)


@login_required
def packing_table(request):
    """Таблица тары, позволяет изменять её количество на складе."""

    table = Packing.objects.all()
    page_obj = paginate_queryset(table, request, ELEMENT_PAGE)
    if request.method == 'POST':
        form = PackingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            packing = get_object_or_404(Packing, id=data['packing'].id)
            if data['operation'] == 'subtract':
                if packing.balance - data['amount'] < 0:
                    form.add_error(None, 'Недостаточно тары на складе!')
                else:
                    packing.balance -= data['amount']
            else:
                packing.balance += data['amount']
            if not form.errors:
                Register.objects.create(
                    operation=data['operation'],
                    amount=data['amount'],
                    text=data['text'],
                    packing=packing,
                    user=request.user
                )
                packing.save()
                return redirect('registration:packing')
    else:
        form = PackingForm()
    context = {
        'button_class': 'btn btn-success btn-sm',
        'page_obj': page_obj,
        'packaging_form': form,
    }
    return render(request, 'registration/packing.html', context)


@login_required
def history_table_client(request, client_id):
    """История возвратов тары для указанного клиента."""

    client = get_object_or_404(Client, pk=client_id)
    table = Extradition.objects.filter(
        client_id=client_id,
    ).select_related('client').order_by('client_id')
    context = {'client': client, 'table': table}
    return render(request, 'registration/history-client.html', context)


@login_required
def report_table(request):
    """Отчет по отгрузкам с ненулевыми остатками тары."""

    extraditions = Extradition.objects.filter(
        balance_storage__gt=0
    ).select_related('client').order_by('client_id')
    page_obj = paginate_queryset(extraditions, request, ELEMENT_PAGE)
    return render(request, 'registration/report.html', {'page_obj': page_obj})


@login_required
def report_table_client(request, client_id):
    """Отчет по отгрузкам для указанного клиента."""

    client = get_object_or_404(Client, id=client_id)
    extradition = Extradition.objects.filter(
        client_id=client_id,
        balance_storage__gt=0
    ).select_related('client').order_by('client_id')
    page_obj = paginate_queryset(extradition, request, ELEMENT_PAGE)
    context = {
        'page_obj': page_obj,
        'client': client
    }
    return render(request, 'registration/report-client.html', context)


@login_required
def report_table_packing(request, packing_id):
    """Отчет по отгрузкам для указанной упаковки."""

    packing = get_object_or_404(Packing, id=packing_id)
    extradition = Extradition.objects.filter(
        packing_id=packing_id,
        balance_storage__gt=0
    ).select_related('packing').order_by('packing_id')
    page_obj = paginate_queryset(extradition, request, ELEMENT_PAGE)
    context = {
        'page_obj': page_obj,
        'packing': packing
    }
    return render(request, 'registration/report-packing.html', context)


@login_required
def report_table_date(request, year, month, day):
    """Отчет по отгрузкам для указанной даты."""

    selected_date = date(year, month, day)
    extradition = Extradition.objects.filter(
        created_at__date=selected_date,
        balance_storage__gt=0
    ).order_by('created_at')
    page_obj = paginate_queryset(extradition, request, ELEMENT_PAGE)
    context = {
        'page_obj': page_obj,
        'created_at': selected_date
    }
    return render(request, 'registration/report-date.html', context)
