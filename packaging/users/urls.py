from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path(
        'personal_account/<int:user_id>/',
        views.personal_account_user,
        name='personal_account'
    ),

]
