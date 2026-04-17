from django import forms
from django.contrib.auth.models import User

class AboutForm(forms.Form):
    about = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        required=False  # El campo es opcional
    )

class ProfileImageForm(forms.Form):
    imagen = forms.ImageField(
        label='Profile Image',
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

class ProfileBannerForm(forms.Form):
    banner = forms.ImageField(
        label='Profile Banner',
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
