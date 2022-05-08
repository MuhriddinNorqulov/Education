from django.contrib import admin
from .models import User, Teacher, Student
from .forms import CustomUserCreationForm, CustomUserChangeForm, TeacherCreationForm
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ['username', 'email', 'role', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'approve')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'approve')}),
    )


@admin.register(Teacher)
class StudentAdmin(admin.ModelAdmin):
    exclude = ['last_login', 'date_joined']
    add_form = TeacherCreationForm


admin.site.register(Student)



