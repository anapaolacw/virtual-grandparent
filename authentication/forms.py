from django import forms
from django.core.exceptions import ValidationError
from .models import User

def password_validator(self,value):
    return False if self.password != value else True

class SignupForm(forms.ModelForm):
    password = forms.CharField(required=True,widget=forms.PasswordInput(), label='Password')
    confirmPassword = forms.CharField(required=True,widget=forms.PasswordInput(), label='Confirm your password')

    def clean_confirmPassword(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirmPassword']:
            raise ValidationError('passwords did not Match.')

    class Meta:
        model = User
        fields = ('name', 'age', 'phoneNumber', 'email','password')
        exclude = ['username',]
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full mt-2 px-4 py-2 rounded-xl'

class LoginForm(forms.ModelForm):
    password = forms.CharField(required=True,widget=forms.PasswordInput(), label='Password2')
    class Meta:
        model = User
        fields = ('email','password')
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full mt-2 px-4 py-2 rounded-xl'