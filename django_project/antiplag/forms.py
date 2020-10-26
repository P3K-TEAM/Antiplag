from django import forms
from .models import File, Paper

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

class TextForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ('title', 'text')
