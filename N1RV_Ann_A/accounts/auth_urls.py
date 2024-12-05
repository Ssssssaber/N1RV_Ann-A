# django/contrib/auth/urls.py
from django.contrib.auth import views
from django.urls import path, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


urlpatterns = [
    # Логин.
    path(
        'login/',
        views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    # Логаут.
    path(
        'logout/',
        views.LogoutView.as_view(template_name='registration/logged_out.html'),
        name='logout'
    ),
    # Изменение пароля.
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'),
        name='password_change'
    ),
    # Сообщение об успешном изменении пароля.
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
    # Восстановление пароля.
    path(
        'password_reset/',
        views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    # Сообщение об отправке ссылки для восстановления пароля.
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    # Вход по ссылке для восстановления пароля.
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    # Сообщение об успешном восстановлении пароля.
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]
