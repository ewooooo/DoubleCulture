
from rest_framework import serializers
from .models import Student, Museum, watch, admin, management

#모델을 json으로 러턴 하기 위해 변경을 위해 필요한 파일 

class StudentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Student 
        fields = ['name', 'student_number', 'password','created', 'feeling']


class MuseumSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Museum 
        fields = ['museum_number', 'howtogo', 'quiz1','quiz2', 'quiz3']



class watchSerializer(serializers.ModelSerializer): 
    class watch: 
        model = watch 
        fields = ['student_number', 'museum_number', 'quiz1_answer','quiz2_answer', 'quiz3_answer']

class adminSerializer(serializers.ModelSerializer): 
    class admin: 
        model = admin 
        fields = ['admin_id', 'password']

class managementSerializer(serializers.ModelSerializer): 
    class management: 
        model = management 
        fields = ['admin_id', 'student_number', 'deleted']
