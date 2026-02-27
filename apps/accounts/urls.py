# apps/accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import (
    StyledAuthenticationForm,
    StyledPasswordResetForm,
    StyledSetPasswordForm,
)

app_name = 'accounts'

urlpatterns = [
    # Registro y perfil
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            authentication_form=StyledAuthenticationForm
        ),
        name='login'
    ),

    # Logout (usa POST desde plantilla; next_page puede ser 'home' o la ruta que prefieras)
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),

    # Flujo de restablecimiento de contraseña
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',
            form_class=StyledPasswordResetForm,
            email_template_name='accounts/password_reset_email.html',
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            form_class=StyledSetPasswordForm
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]