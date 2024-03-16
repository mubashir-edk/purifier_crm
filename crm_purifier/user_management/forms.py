from django import forms
from .models import *

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password']
        
#         widgets = {
#             'username': forms.FileInput(attrs={
#                 'class': 'form-control',
#                 'id': 'formLoginUsername',
#             }),
#             'email': forms.TextInput(attrs={
#                 'class': 'form-control', 
#                 'id': 'formLoginEmail', 
#             }),
#             'password': forms.TextInput(attrs={
#                 'class': 'form-control', 
#                 'id': 'formLoginPassword', 
#             }),
#         }