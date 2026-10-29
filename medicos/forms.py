from django import forms
from .models import RegistroUsuario

class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = RegistroUsuario
        fields = ['nombre_usuario', 'documento', 'puesto', 'microbiologia', 'bacteriologia', 'quimica']
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identificación'}),
            'puesto': forms.Select(attrs={'class': 'form-select'}),
            'microbiologia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bacteriologia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'quimica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        micro = cleaned_data.get('microbiologia')
        bacterio = cleaned_data.get('bacteriologia')
        quimica = cleaned_data.get('quimica')

        if not (micro or bacterio or quimica):
            raise forms.ValidationError("Debe seleccionar al menos un tipo de prueba.")
        return cleaned_data