# Generated by Django 4.2.17 on 2025-01-03 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_client_compani_name_alter_client_last_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'клиента', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'сотрудника', 'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.RenameField(
            model_name='client',
            old_name='compani_name',
            new_name='company_name',
        ),
    ]
