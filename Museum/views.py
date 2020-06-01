from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@csrf_exempt
def Community_page(request,page): #5개씩페이지 page값 url로 받아오기
    if request.method == 'GET':
        query_set = Community.objects.all()[(page-1)*5:] #page번째 글 찾음
        if query_set.count()>=5: # 5개이상 글있으면 5개 글반환
            query_set=query_set[:5]
        serializer = CommunitySerializer(query_set, many =True)
        return JsonResponse(serializer.data, safe= False)


@csrf_exempt
def Community_object(request): 
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommunitySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def Community_ud(request,id): #수정 혹은 삭제할 때는 id url로
    obj = Community.objects.get(pk=id) #수정 혹은 삭제 될 데이터 
    if request.method =='PUT': # PUT이면 수정
        data = JSONParser().parse(request)
        serializer = CommunitySerializer(obj,data = data) #수정 obj도 넣어줌
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE': # DELETE면 삭제
        obj.delete()
        return HttpResponse(status=204)


