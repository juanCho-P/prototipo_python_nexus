from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from .models import Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control'
        })
    )



    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['avatar', 'nombres', 'apellidos', 'username', 'email']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            img = Image.open(avatar)

            # Convertir imagen a RGB si viene en RGBA o P
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Redimensionar la imagen manteniendo una buena calidad de escalado (96x96)
            img = img.resize((96, 96), Image.Resampling.LANCZOS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

       
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{avatar.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
        return avatar

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password, user=self.instance)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')

        return cleaned_data

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['avatar', 'nombres', 'apellidos', 'username', 'email']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

      
        if avatar and isinstance(avatar, UploadedFile):
            img = Image.open(avatar)

            if img.mode != 'RGB':
                img = img.convert('RGB')

           
            img = img.resize((96, 96), Image.Resampling.LANCZOS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{avatar.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )

        return avatar

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password, user=self.instance)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')

        return cleaned_data


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar and isinstance(avatar, UploadedFile):
            img = Image.open(avatar)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            img = img.resize((96, 96), Image.Resampling.LANCZOS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{avatar.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )

        return avatar
    
class EditarPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'username', 'email']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username.strip()) < 7:
            raise ValidationError("El nombre de usuario debe tener mínimo 7 caracteres.")

        if Usuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Nombre de usuario en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este correo ya fue registrado por otro usuario.")
        return email


    class Meta:
        model = Usuario
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            img = Image.open(avatar)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            img = img.resize((96, 96), Image.Resampling.LANCZOS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{avatar.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
        return avatar