from django import forms
from . models import file

class Extrafieldform(forms.ModelForm):
	class Meta:
		model = file
		fields = '__all__'
		
