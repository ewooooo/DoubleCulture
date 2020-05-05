
from rest_framework import serializers
from .models import Museum,StudentProject,Watch
from django.contrib.auth.models import User
#모델을 json으로 러턴 하기 위해 변경을 위해 필요한 파일 


class StudentProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProject
        fields = ['CompleteStatue','created','modify_date']


class MuseumSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Museum 
        fields = ['museum_number', 'howtogo', 'quiz1','quiz2', 'quiz3']


class WatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch
        fields = ['stampStatus', 'quiz1_answer','quiz2_answer', 'quiz3_answer']


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
