from django import forms
from django.utils import timezone
from .models import Evento

class EventoForm(forms.ModelForm):

    class Meta:
        model = Evento
        fields = [
            'imagen',
            'titulo',
            'descripcion',
            'ubicacion',
            'f_inicio',
            'f_fin',
            'categoria',
        ]

        widgets = {
            'imagen': forms.ClearableFileInput(
                attrs={'accept': 'image/*', 'class': 'file-input-custom'}
            ),
            'titulo': forms.TextInput(
                attrs={'placeholder': 'Ej: Torneo de programación', 'class': 'form-input'}
            ),
            'descripcion': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Describe tu evento...', 'class': 'form-textarea'}
            ),
            'ubicacion': forms.TextInput(
                attrs={'placeholder': 'Ej: SENA, Bogotá', 'class': 'form-input'}
            ),
            'f_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-input-date'}
            ),
            'f_fin': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-input-date'}
            ),
            'categoria': forms.CheckboxSelectMultiple(
                attrs={'class': 'category-checkbox-grid'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        f_inicio = cleaned_data.get('f_inicio')
        f_fin = cleaned_data.get('f_fin')
        ahora = timezone.now()

        if f_inicio and f_inicio < ahora:
            self.add_error('f_inicio', 'El evento no puede comenzar en el pasado.')

        if f_fin and f_fin < ahora:
            self.add_error('f_fin', 'El evento no puede finalizar en el pasado.')

        if f_inicio and f_fin and f_fin <= f_inicio:
            self.add_error('f_fin', 'La fecha de finalización debe ser posterior a la de inicio.')

        return cleaned_data