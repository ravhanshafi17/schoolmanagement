from ..models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        # depth = 1
        model = School
        exclude = ['user']

class UserSignUpSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'school')

    def create(self, validated_data):
        school_data = validated_data.pop('school')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_school = True
        user.save()
        school = School.objects.create(user=user, **school_data)
        refresh = RefreshToken.for_user(school)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return user


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['user' , 'school']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'question_type', 'level', 'text', 'marks', 'is_required')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'address', 'phone_number']

class QuestionBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = ['id', 'name', 'subject', 'classes', 'date']

# class QuestionGeneratorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuestionGenerator
#         fields = ('question_type', 'marks_type')
class QuestionGeneratorSerializer(serializers.Serializer):
    question_type = serializers.ListField(child=serializers.CharField())
    marks_type = serializers.ListField(child=serializers.IntegerField())
# class AdminSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
#     class Meta:
#         model = Admin
#         fields = ('id', 'name', 'address', 'phone_number', 'school', 'user')

#     def create(self, validated_data):
#         user = self.context['request'].user
#         school = user
#         print(school)  # Set the school based on the logged-in user's school
#         admin = Admin.objects.create(
#             user=validated_data.get('user'),
#             name=validated_data.get('name'),
#             address=validated_data.get('address'),
#             phone_number=validated_data.get('phone_number'),
#             school=school
#         )
#         return admin
