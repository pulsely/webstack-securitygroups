
from django import forms
from django.forms import widgets
from django.contrib.auth.password_validation import validate_password

class AdminResetForm(forms.Form):
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}),validators=[validate_password])
