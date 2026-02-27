from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseStyledFormMixin:
    """
    Mixin para aplicar atributos comunes a todos los campos de un formulario:
      - class="form-control"
      - placeholder=" " (espacio intencional para :placeholder-shown)
      - conserva autocomplete si ya está definido en el widget
    Úsalo como primer mixin en la herencia de tus formularios personalizados.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            classes = (existing + ' form-control').strip()
            # mantener autocomplete si ya existe
            autocomplete = field.widget.attrs.get('autocomplete')
            attrs = {
                'class': classes,
                'placeholder': ' ',
            }
            if autocomplete:
                attrs['autocomplete'] = autocomplete
            field.widget.attrs.update(attrs)


class StyledAuthenticationForm(BaseStyledFormMixin, AuthenticationForm):
    """
    AuthenticationForm con estilos aplicados desde el mixin.
    Úsalo en LoginView con authentication_form=StyledAuthenticationForm.
    """
    pass


class StyledPasswordResetForm(BaseStyledFormMixin, PasswordResetForm):
    """
    PasswordResetForm estilizado.
    Úsalo en PasswordResetView con form_class=StyledPasswordResetForm.
    """
    pass


class StyledSetPasswordForm(BaseStyledFormMixin, SetPasswordForm):
    """
    SetPasswordForm estilizado (usado en password reset confirm).
    """
    pass


class StyledUserCreationForm(BaseStyledFormMixin, UserCreationForm):
    """
    UserCreationForm estilizado para registro.
    Puedes extenderlo para añadir campos adicionales si tu User model los requiere.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


# Ejemplo opcional: formulario para editar perfil (si tienes un Profile model o campos en User)
class ProfileForm(BaseStyledFormMixin, forms.ModelForm):
    """
    Formulario de ejemplo para editar campos de perfil.
    Ajusta 'Profile' y los campos según tu implementación real.
    """
    class Meta:
        model = User  # Cambia por tu modelo Profile si lo usas
        fields = ['first_name', 'last_name', 'email']  # añade otros campos si aplica

    # Si necesitas validaciones adicionales, añádelas aquí
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email__iexact=email).exclude(pk=getattr(self.instance, 'pk', None))
            if qs.exists():
                raise forms.ValidationError("Este correo ya está en uso.")
        return email