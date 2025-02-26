from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from .models import (
    Packing,
    Extradition,
    Comeback,
    Register,
    Cancellation
)
from django.contrib.auth.models import Group

admin.site.site_header = _("Панель администратора ")  # Название в заголовке страницы
admin.site.site_title = _("Панель администратора")  # Название в заголовке браузера
admin.site.index_title = _("Добро пожаловать в панель администратора")  # Заголовок на главной странице админки


@admin.register(Packing)
class PackingAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')
    search_fields = ('name',)
    fields = ('name', 'text')

# @admin.register(Extradition)
# class ExtraditionAdmin(admin.ModelAdmin):
#     list_display = ('packing', 'client', 'created_at', 'text')
#     search_fields = ('packing__name', 'client', 'user__username')
#     exclude = ('user',)

#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         super().save_model(request, obj, form, change)


# @admin.register(Comeback)
# class ComebackAdmin(admin.ModelAdmin):
#     list_display = ('packing', 'client', 'created_at', 'amount',)
#     search_fields = ('packing__name', 'client', 'user__username')
#     exclude = ('user',)

#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         super().save_model(request, obj, form, change)


# @admin.register(Register)
# class RegisterAdmin(admin.ModelAdmin):
#     list_display = ('packing', 'created_at', 'text')
#     search_fields = ('packing__name', 'user__username')
#     exclude = ('user',)

#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         super().save_model(request, obj, form, change)


# @admin.register(Cancellation)
# class CancellationAdmin(admin.ModelAdmin):
#     list_display = ('packing', 'created_at', 'text')
#     search_fields = ('packing__name', 'user__username')
#     exclude = ('user',)

#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         super().save_model(request, obj, form, change)


admin.site.unregister(Group)
