from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    user_id = forms.CharField(max_length=30, required=True)
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'password1', 'password2')

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        if User.objects.filter(user_id=user_id).exists():
            raise forms.ValidationError("User ID already exists")
        return user_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
