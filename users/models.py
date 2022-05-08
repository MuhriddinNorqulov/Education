from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import UserRole
from .manager import TeacherManager, StudentManager, AdminManager


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRole.choices())
    approve = models.BooleanField(default=False)


class Teacher(User):
    objects = TeacherManager()


    class Meta:
        proxy = True


class Student(User):
    objects = StudentManager()


    class Meta:
        proxy = True


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True


