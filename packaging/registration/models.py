from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKey,
    Model,
    TextField,
)

from users.models import Client, User

CHAR_MAX = 128


class Packing(Model):
    """Тара"""

    name = CharField(
        'Наименование',
        max_length=CHAR_MAX,
        db_index=True,
    )
    text = TextField(
        'Комментарий',
        null=True,
        blank=True,
    )
    balance = IntegerField(
        'в наличии',
        default=0,
    )

    class Meta:
        verbose_name = 'тару'
        verbose_name_plural = 'Тара'

    def __str__(self):
        return self.name


class BaseClass(Model):
    """Базовый класс: Приход/Списание"""

    packing = ForeignKey(
        Packing,
        on_delete=CASCADE,
        verbose_name='Тара',
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
    )
    created_at = DateTimeField(
        'Дата записи',
        auto_now_add=True,
    )
    amount = IntegerField(
        'Количество',
        null=False,
        blank=False,
    )
    text = TextField(
        'Комментарий',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Extradition(BaseClass):
    """Выдача клиенту"""

    client = ForeignKey(
        Client,
        on_delete=CASCADE,
        verbose_name='Клиент',
    )
    balance_storage = IntegerField(
        'Остаток',
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'Выдача'
        verbose_name_plural = 'Выдача'

    def __str__(self):
        return f'Выдача от {self.created_at.date()} для {self.client}'


class Comeback(BaseClass):
    """Возврат на склад"""

    client = ForeignKey(
        Client,
        on_delete=CASCADE,
        verbose_name='Клиент',
    )

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возврат'

    def __str__(self):
        return f'Возврат от {self.created_at.date()} для {self.client}'


class Register(BaseClass):
    """Оприходование на склад"""

    operation = TextField(
        'Комментарий',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Оприходование'
        verbose_name_plural = 'Оприходование'

    def __str__(self):
        return f'Оприходование: {self.packing.name}, {self.amount} шт.'


class Cancellation(BaseClass):
    """Списание тары"""

    class Meta:
        verbose_name = 'Списание'
        verbose_name_plural = 'Списание'

    def __str__(self):
        return f'Списание: {self.packing.name}, {self.amount} шт.'


@receiver(pre_save, sender=BaseClass)
def set_user(sender, instance, **kwargs):
    if not instance.user:
        instance.user = instance._current_user  # Или другой механизм получения текущего пользователя