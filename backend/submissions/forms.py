from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'url', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

    # Método para validar los datos del formulario
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        url = cleaned_data.get('url')
        text = cleaned_data.get('text')

        # Validación: el título es obligatorio
        if not title:
            self.add_error('title', 'Title is required.')

        # Validación: si no hay URL, el texto es obligatorio
        if not url and not text:
            self.add_error('text', 'Text is required if no URL is provided.')
        
class EditSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'text']  # Excluir 'url'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    # Método para validar los datos del formulario
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        # Validación: el título es obligatorio
        if not title:
            self.add_error('title', 'Title is required.')