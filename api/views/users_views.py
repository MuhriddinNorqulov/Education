from datetime import datetime
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework_simplejwt.views import TokenObtainPairView
from api.permissions import IsStudent, IsTeacher, IsAuthorOrIsAdmin, TeacherUpdatePermission, IsAdminOrReadOnly
from api.serializers import (
    UserSerializerWithToken,
    UserRegistrationSerializer,
    UserSerializer,
    TeacherSerializer,
    StudentSerializer,
    TeacherProfileSerializer,
    StudentProfileSerializer
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
    ListAPIView
)
from users.models import User, Teacher, Student
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from course.models import Course


class AdminProfile(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        serializer = UserSerializer(request.user, many=False)
        return serializer.data


class StudentProfile(APIView):
    permission_classes = [IsStudent]

    def get(self, request):

        student = Student.objects.get(id=request.user.id)
        serializer = StudentProfileSerializer(student, many=False)
        return Response(serializer.data)

    def post(self, request):
        student = Student.objects.get(id=request.user.id)

        course_id = request.data['course_id']
        course = get_object_or_404(Course, id=course_id)
        print(course)
        course.students.add(student)
        course.save()

        serializer = StudentSerializer(request.user, many=False)
        return Response(serializer.data)


class TeacherProfile(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        teacher = Teacher.objects.get(id=request.user.id)
        serializer = TeacherProfileSerializer(teacher, many=False)

        return Response(serializer.data)


class UserRegistrationApiView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        if serializer.validated_data['role'] == 'admin' and not self.request.user.is_staff:
            raise PermissionDenied

        else:
            serializer.save()


class TeacherListApiView(ListCreateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Teacher.objects.all()


class StudentListApiView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Student.objects.all()


class UsersListApiView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()


class TeacherUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [TeacherUpdatePermission]

    queryset = Teacher.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #
    #     # Add custom claims
    #     token['name'] = user.username
    #     token['key'] = 'val'
    #     # ...
    #
    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        self.user.last_login = datetime.now()
        self.user.save()
        # del data['refresh']
        for key, val in serializer.items():
            data[key] = val

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer