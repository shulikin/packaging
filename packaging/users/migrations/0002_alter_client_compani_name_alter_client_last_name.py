# Generated by Django 4.2.17 on 2024-12-11 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='compani_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия'),
        ),
    ]
