from django.db import models
from users.models import Teacher, Student
# Create your models here.


class Course(models.Model):
    owner = models.ForeignKey(Teacher, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.title


