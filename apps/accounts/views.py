from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .forms import StyledUserCreationForm, ProfileForm


def register(request):
    """
    Registro de usuario.
    Usa StyledUserCreationForm (aplica clases y placeholder en forms.py).
    Al crear el usuario redirige a la página de login (o inicia sesión automáticamente si lo prefieres).
    """
    if request.method == 'POST':
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cuenta creada correctamente. Ya puedes iniciar sesión.")
            return redirect('accounts:login')  # la vista de login suele venir de django.contrib.auth.urls
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = StyledUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """
    Muestra la página de perfil del usuario.
    La plantilla espera `user` y `profile` (si existe).
    """
    # Si tu proyecto tiene un modelo Profile relacionado por OneToOneField:
    profile = getattr(request.user, 'profile', None)
    return render(request, 'accounts/profile.html', {'user': request.user, 'profile': profile})


@login_required
def profile_edit(request):
    """
    Editar perfil. Intenta usar ProfileForm si existe; si ProfileForm está basado en User,
    lo usará con instance=request.user. Si tu proyecto tiene un modelo Profile separado,
    ajusta ProfileForm para usar instance=request.user.profile y guarda ambos objetos.
    """
    # Intentamos usar ProfileForm con la instancia adecuada.
    # Si ProfileForm está diseñado para User, usamos request.user; si está diseñado para Profile,
    # intentamos usar request.user.profile.
    form_instance = None
    profile_instance = getattr(request.user, 'profile', None)

    # Determinar la instancia que espera el formulario
    try:
        # Si ProfileForm.Meta.model es User, instance=request.user funcionará.
        form = ProfileForm(instance=request.user if profile_instance is None else profile_instance)
    except Exception:
        # Fallback: crear el formulario sin instancia
        form = ProfileForm()

    if request.method == 'POST':
        # Si el formulario corresponde al Profile model y existe profile_instance, pasamos files y instance
        if profile_instance is not None and hasattr(ProfileForm.Meta, 'model') and ProfileForm.Meta.model != request.user.__class__:
            form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        else:
            # Asumimos que ProfileForm edita campos del User
            form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            obj = form.save(commit=False)
            # Si el formulario edita el User, guardamos user; si edita profile, guardamos profile.
            obj.save()
            # Si el profile no existía y el form creó uno, enlazarlo al usuario si aplica
            if profile_instance is None and hasattr(obj, 'user') and obj.user is None:
                try:
                    obj.user = request.user
                    obj.save()
                except Exception:
                    pass
            messages.success(request, "Perfil actualizado correctamente.")
            return HttpResponseRedirect(reverse_lazy('accounts:profile'))
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")

    return render(request, 'accounts/profile_edit.html', {'form': form})