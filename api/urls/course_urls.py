from django.urls import path
from api.views import course_views as views

urlpatterns = [
    path('create', views.CourseCreateApiView.as_view(), name='course-create'),
    path('<int:pk>', views.CourseDetailApiView.as_view()),

]