from django import forms
from django.forms import ModelForm
from tinymce.models import HTMLField

from .models import Image


class MoveImageForm(ModelForm):
	class Meta:
		model = Image
		fields = ['gallery']
		labels = {
			'gallery': '',
		}

class NewImageForm(ModelForm):
	class Meta:
		model = Image
		fields = ['gallery', 'name', 'dscr', 'image']
		labels = {
			'gallery': 'Galerie:',
			'name': 'Titulek:',
			'dscr': 'Popis:',
			'image': 'Soubor obrázku:'
		}
		widgets = {
			'image': forms.FileInput(attrs={})
		}
