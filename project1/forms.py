from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from auth_module.models import registered_user

class register_user_form(forms.ModelForm):
    class Meta:
        model = registered_user
        fields = ['username','email','password']
        # fields = ('username','email','password')
        widgets = {
        'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Account'))
