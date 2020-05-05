from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Museum(models.Model):
    museum_number = models.CharField(max_length=13, primary_key=True)
    howtogo = models.CharField(max_length=20)
    quiz1 = models.CharField(max_length=50)
    quiz2 = models.CharField(max_length=50)
    quiz3 = models.CharField(max_length=50)

    class Meta:
       ordering = ['museum_number']


class StudentProject(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CompleteStatue = models.BooleanField(default=False) # 이수 여부

    created = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)  # 수정일

    class Meta:
        ordering = ['created']


class Watch(models.Model):
    user = models.ForeignKey(StudentProject, on_delete=models.CASCADE,null=True)  # 만든 유저
    museum = models.OneToOneField(Museum, on_delete=models.CASCADE,null=True)     # 해당 박물관

    stampStatus = models.BooleanField(default=False)                                 # 스탬프 상태
 #   create_Stamp_date = models.DateTimeField(Null=True)                              # 스팸프 장소
    quiz1_answer = models.CharField(max_length=50, default=" ")                      # 퀴즈에 대한 답변
    quiz2_answer = models.CharField(max_length=50, default=" ")
    quiz3_answer = models.CharField(max_length=50, default=" ")

    create_date = models.DateField(auto_now_add=True,null=True)                   # 생성일
    modify_date = models.DateField(auto_now=True)                       # 수정일

    class Meta:
       ordering = ['modify_date']