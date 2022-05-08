
from django.db.models import manager
from django.contrib.auth.models import UserManager


class TeacherManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="teacher")


class StudentManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="student")


class AdminManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='admin', is_staff=True)
