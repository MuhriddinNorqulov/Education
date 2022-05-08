
from api.views import users_views as views
from django.urls import path


urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view(), name='login'),
    path('register', views.UserRegistrationApiView.as_view(), name='register'),

    path('<int:pk>', views.UserUpdateApiView.as_view(), name='user-update'),

    path('users-list', views.UsersListApiView.as_view(), name='users-list'),

    path('teacher-list', views.TeacherListApiView.as_view(), name='teacher-list'),
    path('teacher/<int:pk>', views.TeacherUpdateApiView.as_view(), name='teacher-update'),

    path('student-list', views.StudentListApiView.as_view(), name='student-list'),

    path('teacher-profile/', views.TeacherProfile.as_view(), name='teacher-profile'),

    path('student-profile', views.StudentProfile.as_view(), name='student-profile'),

    path('admin-profile', views.AdminProfile.as_view(), name='student-profile'),
]