from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Teacher


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'role', 'approve']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User

        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role', 'approve']


class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'role', 'approve']


