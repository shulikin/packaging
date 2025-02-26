from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Поля для отображения в списке пользователей
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'position',
        'phone_number',
        'is_staff',
        'created_at'
    )
    list_filter = (
        'position',
        'is_staff',
        'is_superuser',
        'is_active'
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number'
    )
    ordering = ('created_at',)

    # Поля в деталях пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'address',
                'avatar',
                'position'
            )
        }),
        # ('Разрешения', {
        #     'fields': (
        #         'is_active', 'is_staff', 'is_superuser', 
        #         'groups', 'user_permissions',
        #     )
        # }),
        ('Важные даты', {'fields': (
            'last_login',
            'date_joined',
            'created_at',
            'updated_at'
        )}),
    )

    # Поля при создании пользователя в админке
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'address',
                'avatar',
                'position',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            ),
        }),
    )

    # Отображение только для чтения
    readonly_fields = (
        'created_at',
        'updated_at',
        'last_login',
        'date_joined'
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'phone_number',
        'company_name',  # Добавлено в список
    )

    # Метод для отображения company_name, если оно вычисляется
    def company_name(self, obj):
        return obj.company.name if obj.company else '—'
    company_name.short_description = 'Company Name'  # Заголовок столбца в админке
