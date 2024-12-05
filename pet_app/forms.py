# forms.py
from django import forms
from .models import Pet ,Products ,User

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'age','category', 'pic', 'price', 'description', 'breed', 'color', 'stock_level','vaccination']

        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),  # Category as dropdown
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class':'form-control'}),
            'pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'vaccination':forms.TextInput(attrs={'class':'form-control'}),
            
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'category', 'pic', 'price', 'description', 'stock_level']

        # Customize the widgets
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for categories
            'pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name','mobile', 'email', 'is_expert', 'is_seller', 'role']