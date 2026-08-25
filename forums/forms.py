from django import forms
from .models import Foro

class ForoForm(forms.ModelForm):

    class Meta:
        model = Foro

        
        fields = [
            'titulo',
            'imagen',
            'categoria',
            'descripcion',
        ]

        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'placeholder': 'Ej: ¿Cómo estructurar microservicios en Spring Boot?'
                }
            ),

            'imagen': forms.ClearableFileInput(
                attrs={
                    'accept': 'image/*',
                    'onchange': 'previewImage(event)'
                }
            ),

            'categoria': forms.CheckboxSelectMultiple(),

            'descripcion': forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder': 'Escribe el contexto, dudas o tema central de discusión...'
                }
            ),
        }

    def clean_categoria(self):
        categorias = self.cleaned_data.get('categoria')
        if not categorias:
            raise forms.ValidationError('Debes seleccionar al menos una categoría.')
        return categorias