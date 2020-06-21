from rest_framework import serializers
from .models import institution,Student,Watch,Community
from django.contrib.auth.models import User
#모델을 json으로 러턴 하기 위해 변경을 위해 필요한 파일


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['CompleteState','created','modify_date']


class institutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = institution
        fields = ['institution_number', 'quiz1','quiz2','quiz3']


class WatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch
        fields = ['stampStatus', 'quiz_answer']


# class userSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#
#         fields = ['username', 'email', 'first_name', 'last_name']
#         read_only_fields = ['username']

class userCustomSerializer(serializers.ModelSerializer):
    student_data = serializers.SerializerMethodField()

    def get_student_data(self, obj):
        return obj.student.CompleteState

    class Meta:
        model = User

        fields = ['username', 'email', 'first_name','student_data']
        read_only_fields = ['username']

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id','author','text']

class Watch_stampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch
        fields = ['stampStatus']

class feelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['feeling']