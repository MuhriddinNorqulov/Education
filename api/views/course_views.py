from datetime import datetime
from rest_framework.response import Response
from api.serializers import CourseSerializer, TeacherSerializer, StudentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.permissions import IsTeacher, IsAuthorOrIsAdmin
from course.models import Course
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CourseCreateApiView(ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher]
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseDetailApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = CourseSerializer
    permission_classes = [IsAuthorOrIsAdmin]

    queryset = Course.objects.all()





