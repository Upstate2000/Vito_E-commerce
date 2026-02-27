from django import forms
from .models import Category

class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Buscar', widget=forms.TextInput(attrs={'placeholder':'Buscar productos...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label='Todas las categorías')