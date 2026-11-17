from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import Usuario

# bcrypt con el mismo costo (12) que usa el backend NestJS (usuarios.service.ts:
# `const saltOrRounds = 12`), para que bcrypt.compare del login valide el hash.
import bcrypt


class UsuarioForm(forms.ModelForm):
    """
    Formulario de Usuario con gestión de contraseña "write-only".

    El campo `password_hash` NO se muestra ni se editable: la contraseña nueva
    se ingresa en `nueva_password` en plano y aquí se guarda hasheada con bcrypt.
    Sirve tanto para crear usuarios como para cambiar la contraseña de uno existente.
    """

    nueva_password = forms.CharField(
        label="Contraseña",
        required=False,
        widget=forms.PasswordInput(
            render_value=False,
            attrs={"placeholder": "Mínimo 8 caracteres", "autocomplete": "new-password"},
        ),
        help_text=(
            "Déjala vacía para no cambiarla. "
            "Se guarda cifrada (bcrypt) exactamente como la valida el backend al iniciar sesión."
        ),
    )

    class Meta:
        model = Usuario
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aviso de estado real de la contraseña para orientar al administrador.
        if self.instance and self.instance.pk:
            if self.instance.password_hash:
                self.fields["nueva_password"].help_text = (
                    "Este usuario YA tiene contraseña; si escribes una nueva la reemplazas. "
                    "Déjala vacía para mantener la actual."
                )
            else:
                self.fields["nueva_password"].help_text = (
                    "⚠ Este usuario NO tiene contraseña: no podrá iniciar sesión "
                    "hasta que definas una aquí (mínimo 8 caracteres)."
                )

    def clean_nueva_password(self):
        password = self.cleaned_data.get("nueva_password") or ""
        if not password:
            return ""
        # Validadores de Django (largo, contraseñas comunes, numéricas, similar al email/nombre).
        validate_password(password, user=self.instance if self.instance.pk else None)
        return password

    @staticmethod
    def hashear(password: str) -> str:
        """Hashea la contraseña en plano con bcrypt (cost 12), listo para password_hash."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("ascii")
