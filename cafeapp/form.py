from django import forms
from .models import MainItem

class MainItemForm(forms.ModelForm):
    class Meta:
        model = MainItem
        fields = ['productName', 'Discription', 'price', 'quantity', 'image']
        widgets = {
            'productName': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; margin-bottom: 15px;'  # Set width to 80% for productName
            }),
            'Discription': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%; height: 80px; margin-bottom: 15px;'  # Set width to 80% for description and height
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; margin-bottom: 15px;'  # Set width to 80% for price
            }),
            
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; margin-bottom: 15px;'  # Set width to 80% for price
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; margin-bottom: 15px;'  # Set width to 80% for image upload
            }),
        }
