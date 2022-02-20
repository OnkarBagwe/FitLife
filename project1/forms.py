from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
#from auth_module.models import registered_user

"""class register_user_form(forms.ModelForm):
    class Meta:
        model = registered_user
        fields = ['username','email','password']
        # fields = ('username','email','password')
        #REQUIRED_FIELDS = ['username','email','password']

        widgets = {
        'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Account'))"""
        



from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class register_user_form(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),

        }


class login_user_form(AuthenticationForm):

    class Meta:
        model = User
        fields = ["username", "password"]