from django import forms

from .models import Packing, Extradition, Register


class PackingForm(forms.ModelForm):
    OPERATION_CHOICES = [
        ('add', 'Ввод в эксплуатацию'),
        ('subtract', 'Списание'),
    ]

    operation = forms.ChoiceField(
        choices=OPERATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Операция"
    )

    class Meta:
        model = Register
        fields = ['packing', 'operation', 'amount', 'text']
        widgets = {
            'packing': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество',
                'min': '0',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите комментарий',
                'rows': 3,
            }),
        }


class FormExtradition(forms.ModelForm):
    class Meta:
        model = Extradition
        # fields = '__all__'  # Используем все поля модели
        fields = ['packing', 'amount', 'text', 'client', ]
        widgets = {
            'packing': forms.Select(attrs={
                'class': 'form-select',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество',
                'min': '0',  # Минимальное значение
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите комментарий',
                'rows': 3,
            }),
            'client': forms.HiddenInput(attrs={
                'value': ''  # Значение будет установлено в представлении
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем лейблы с каждого поля
        self.fields['packing'].empty_label = 'Выбрать'


class ClientForm(forms.Form):
    CHOICE = [
        ('extradition', 'Отгрузка оборотной тары Клиенту'),
        ('refund', 'Возврат тары на склад предприятия'),
    ]

    # Поле с радиокнопками
    move = forms.ChoiceField(
        choices=CHOICE,
        label='',
        widget=forms.RadioSelect(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Пожалуйста, выберите одну из опций.',
        },
        required=True,
    )
    packing = forms.ModelChoiceField(
        label='',
        queryset=Packing.objects.all(),
        empty_label="Наименование тары",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.IntegerField(
        min_value=1,  # Убедимся, что количество больше 0
        max_value=9999,  # Ограничим максимальное количество (по необходимости)
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введите количество',
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Это поле обязательно для заполнения.',
            'invalid': 'Введите корректное количество (целое число).',
            'min_value': 'Количество не может быть меньше 1.',
            'max_value': 'Количество не может быть больше 9999.',
        }
    )


class ComebackForm(forms.Form):
    balance_amount = forms.IntegerField(min_value=1)
    text = forms.CharField(max_length=255, required=False)
    client_id = forms.IntegerField()
    packing_id = forms.IntegerField()
    extradition_id = forms.IntegerField()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     balance_storage = cleaned_data.get('balance_storage')
    #     balance_amount = cleaned_data.get('balance_amount')

    #     # if balance_amount > balance_storage:
    #     #     raise forms.ValidationError("Число возврата превышает балансовый остаток.")
    #     # return cleaned_data
