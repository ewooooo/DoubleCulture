from django.db import models
from django.contrib.auth.models import User
from django_db_views.db_view import DBView  # pip install django-db-views , installed app='django_db_views',


# Create your models here.


class institution(models.Model):
    institution_number = models.CharField(max_length=13, primary_key=True)
    quiz1 = models.CharField(max_length=400,blank=True, default=False)
    quiz2= models.CharField(max_length=400,blank=True, default=False)
    quiz3 = models.CharField(max_length=400, blank=True, default=False)
    qrcode=models.CharField(max_length=50, default=False)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    gps_error= models.CharField(max_length=5, default=0.5)
    class Meta:
        ordering = ['institution_number']



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CompleteState = models.BooleanField(default=False)  # 이수 여부
    feeling= models.TextField(default='30Bytes 이상 입력하세요')
    created = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)  # 수정일

    class Meta:
        ordering = ['created']



class Watch(models.Model):
    Watch_Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)  # 만든 유저
    Watch_institution = models.ForeignKey(institution, on_delete=models.CASCADE, null=True)  # 해당 박물관

    stampStatus = models.BooleanField(default=False)  # 스탬프 상태
    create_Stamp_date = models.DateField(null=True)
    create_Stamp_time = models.TimeField(null=True)  # 스팸프 장소

    quiz_answer = models.CharField(max_length=400, default=" ")  # 퀴즈에 대한 답변


    modify_date = models.DateField(auto_now=True)  # 수정일

    class Meta:
        ordering = ['modify_date']


class Community(models.Model):
    author= models.CharField(max_length=50, default=" ")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']


class joinkey(models.Model):  # crontab 검색해서 주기마다 실행되는코드 짜기
    key = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class Total(DBView):
    # view_definition 쿼리문 작성하면된다.
    view_definition = """
    select * from Museum_Watch
    """

    class Meta:
        managed = False
        db_table = "Total"