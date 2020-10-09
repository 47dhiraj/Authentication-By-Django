from django import forms
from django.contrib.auth.models import User



class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=254, help_text='Required',error_messages={"required": "Username is required"})
    first_name = forms.CharField(max_length=30, required=False, error_messages={"required": "First Name is required"})
    last_name = forms.CharField(max_length=30, required=False, error_messages={"required": "Last Name is required"})
    email = forms.EmailField(max_length=254, help_text='Required', error_messages={"required": "Email is required"})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)