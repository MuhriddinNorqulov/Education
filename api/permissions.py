from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in list(SAFE_METHODS):
            return True

        return bool(request.user and request.user.is_staff)


class IsStudent(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.role == 'student'


class TeacherUpdatePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in list(SAFE_METHODS):
            return True
        return bool(request.user.is_staff or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in list(SAFE_METHODS):
            return True

        if 'approve' in request.data.keys():
            return request.user.is_staff
        return obj == request.user


class IsTeacher(BasePermission):

    def has_permission(self, request, view):

        return request.user.role == "teacher" and request.user.approve == True



class IsAuthorOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in list(SAFE_METHODS):
            return True

        return obj.owner == request.user or request.user.is_staff == True


