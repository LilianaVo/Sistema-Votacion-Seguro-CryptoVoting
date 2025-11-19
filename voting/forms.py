from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class CustomRegisterForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@ejemplo.com'}),
        label="Correo Electrónico"
    )
    # --- AQUÍ ESTÁ EL CAMBIO ---
    password = forms.CharField(
        min_length=8,  # <--- ESTO FALTABA: Fuerza el mínimo de 8 caracteres
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
        label="Contraseña",
        error_messages={'min_length': 'La contraseña debe tener al menos 8 caracteres.'}
    )
    # ---------------------------
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        """
        Verifica que el correo no exista ya en la base de datos.
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(username=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado. Por favor inicia sesión.")
        return email

    def clean(self):
        """Verifica que las contraseñas coincidan."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        """
        Guarda el usuario usando el email como username.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre@ejemplo.com'}),
        label="Correo Electrónico"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
        label="Contraseña"
    )

    def clean(self):
        """
        Autentica usando el email como username.
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = None
            # Intentamos autenticar asumiendo que el username ES el email
            from django.contrib.auth import authenticate
            self.user_cache = authenticate(self.request, username=username, password=password)
            
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Correo electrónico o contraseña incorrectos."
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Esta cuenta está inactiva.")
        
        return self.cleaned_data
    
class KeyCheckForm(forms.Form):
    private_key = forms.FileField(
        label="Selecciona tu archivo de Llave Privada (.key)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.key,.pem'}),
        help_text="Sube el archivo que descargaste al generar tu llave. No guardaremos este archivo."
    )