# forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'dob', 'age', 'phoneno', 'password1', 'password2')

class CustomUserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'middle_name', 'last_name', 'dob', 'age', 'phoneno']