from rest_framework import serializers
from users.models import User, Student, Teacher
from course.models import Course
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        exclude = ["approve", "is_superuser", "is_active", "groups", "user_permissions", 'last_login', 'date_joined']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        print('validate data ///', validated_data)
        if validated_data['role'] == 'admin':
            validated_data['is_staff'] = True
        else:
            validated_data['is_staff'] = False

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            is_staff=validated_data['is_staff']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'last_login']


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'role', 'approve', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'username', 'email', 'approve', 'first_name', 'last_name', 'last_login']


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    students = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Course
        fields = '__all__'

    def get_owner(self, obj):

        serializer = TeacherSerializer(obj.owner, many=False)

        return serializer.data

    def get_students(self, obj):
        serializer = StudentSerializer(obj.students, many=True)
        return serializer.data


class TeacherProfileSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Teacher
        fields = ['username', 'email', 'first_name', 'last_name', 'last_login', 'course']

    def get_course(self, obj):
        courses = obj.courses.all()
        serializer = CourseSerializer(courses, many=True)
        for i in serializer.data:
            del i['owner']
        return serializer.data


class StudentProfileSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['username', 'email', 'first_name', 'last_name', 'courses']


    def get_courses(self, obj):
        courses = Course.objects.filter(students=obj)
        serializer = CourseSerializer(courses, many=True)
        for i in serializer.data:
            del i['students']
        return serializer.data