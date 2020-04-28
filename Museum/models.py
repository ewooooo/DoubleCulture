from django.db import models

# Create your models here.

class Student(models.Model):
    name =models.CharField(max_length=10)
    student_number= models.CharField(max_length=13, primary_key=True)
    password=models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    feeling =models.CharField(max_length=500)
    class Meta:
        ordering = ['student_number']


class Museum(models.Model):
    museum_number= models.CharField(max_length=13, primary_key=True)
    howtogo=models.CharField(max_length=20)
    quiz1 =models.CharField(max_length=50)
    quiz2 =models.CharField(max_length=50)
    quiz3 =models.CharField(max_length=50)
    class Meta:
       ordering = ['museum_number']


class watch(models.Model):
    student_number= models.CharField(max_length=13)
    museum_number= models.CharField(max_length=13)
    auth=models.CharField(max_length=1)
    quiz1_answer =models.CharField(max_length=50)
    quiz2_answer =models.CharField(max_length=50)
    quiz3_answer =models.CharField(max_length=50)
    class Meta:
       ordering = ['student_number']