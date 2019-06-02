from django import forms
from .models import UrlInput

class UrlInputForm(forms.ModelForm):
    class Meta:
        model = UrlInput
        fields = ('url',)