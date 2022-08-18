from dataclasses import field
from itertools import product
from django import forms
from . import models
class FormProducts(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name','description','image','price','stock']
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'description':forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'image':forms.FileInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'price':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'min':1,
                    'value':0
                }
            ),
            'stock':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'min':0,
                    'value':0
                }
            ),
        }