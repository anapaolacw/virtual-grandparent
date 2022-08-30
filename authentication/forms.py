from django import forms
from django.core.exceptions import ValidationError
from .models import User
from functools import partial

def password_validator(self,value):
    return False if self.password != value else True

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            # add form-control class to all fields
            field.widget.attrs['class'] = 'form-control'
            # set icon attr on field object
            if field_name in icons:
                field.icon = icons[field_name]
class SignupForm(BootstrapModelForm):
    name= forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Full name'}))
    email= forms.CharField(widget= forms.EmailInput
                           (attrs={'placeholder':'Email'}))
    phoneNumber= forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Phone Number'}), max_length=11)
    password = forms.CharField(required=True, widget=forms.PasswordInput
                                            (attrs={'placeholder':'Password'}))
    confirmPassword = forms.CharField(required=True,widget=forms.PasswordInput
                                            (attrs={'placeholder':'Confirm your Password'}))
    dateOfBirth = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    
    isHelper = forms.BooleanField(required=False, label='Sign up as a helper')
   
    def clean_confirmPassword(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirmPassword']:
            raise ValidationError('passwords did not Match.')

    class Meta:
        model = User
        # fields = ('name', 'age', 'phoneNumber', 'email','password')
        fields = ('name', 'email', 'phoneNumber','password')
        exclude = ['username',]
        icons = {
            'name': 'fa fa-user',
            'password': 'fa fa-lock',
            'confirmPassword': 'fa fa-lock',
            'email': 'fa fa-envelope',
            'phoneNumber': 'fa fa-phone',
            'dateOfBirth': 'fa fa-calendar'
        }
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type == 'checkbox':
                visible.field.widget.attrs['class'] = 'm-2 blue-checkbox'
            elif visible.field.icon == 'fa fa-calendar':
                visible.field.widget.attrs['class'] = 'w-full mt-2 px-4 py-2 rounded-xl pl-12 datepicker'
            else:
                visible.field.widget.attrs['class'] = 'w-full mt-2 px-4 py-2 rounded-xl pl-12'

class LoginForm(BootstrapModelForm):
    email= forms.CharField(widget= forms.EmailInput
                           (attrs={'placeholder':'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput
                                            (attrs={'placeholder':'Password'}), label='Password')
    class Meta:
        model = User
        fields = ('email','password')
        icons = {
            'email': 'fa fa-envelope',
            'password': 'fa fa-lock',
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full mt-2 px-4 py-2 rounded-xl pl-12'
