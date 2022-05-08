from enum import Enum

class UserRole(Enum):
    teacher = 'teacher'
    student = 'student'
    admin = 'admin'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)