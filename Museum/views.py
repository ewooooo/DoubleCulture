from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

@csrf_exempt
def viewMuseum(request):
    if request.method == 'GET':
        data = JSONParser().parse(request)
        museum_number = data['museum_number']
        museum = Museum.objects.get(museum_number=museum_number)
        museumSeri = MuseumSerializer(museum)

        return JsonResponse(museumSeri.data, safe=False)

@csrf_exempt
def setMuseum(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MuseumSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def id_overlap_check(request):
    if request.method == 'GET':
        data = JSONParser().parse(request)
        username = data['username']
        try:
            # 중복 검사 실패
            user = User.objects.get(username=username)
        except:
            # 중복 검사 성공
            user = None
        if user is None:
            overlap = "pass"
        else:
            overlap = "fail"
        context = {'overlap': overlap}
        return JsonResponse(context)


@csrf_exempt
def singUp(request):
    if request.method == 'GET':
        return JsonResponse({'message': '회원가입 완료'}, status=200)
    if request.method == 'POST':
        data = JSONParser().parse(request)

        username = data['username']
        password = data['password']
        re_password = data['re_password']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']

        if not(username and password and re_password and email and first_name and last_name) :
            return JsonResponse({'error': '빈칸'}, status=200)
        elif password !=re_password:
            return JsonResponse({'error': '비번 다름'}, status=200)
        else:
            createuser = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            p = StudentProject(user = createuser)
            p.save()
            for a in Museum.objects.all():
                w = Watch(project=p, museum=a)
                w.save()
            return JsonResponse({'message': '회원가입 완료'}, status=200)

@csrf_exempt
def MainPageUserData(request):
    # 로그인 하면 셰션 리턴
    if request.method == 'GET':
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']

        loginStatus = authenticate(username=username, password=password)
        if loginStatus :
            # 로그인 성공
            user = User.objects.get(username=username)
            userSeri = userSerializer(user)    # user 정보

            project = user.studentproject
            projectSeri = StudentProjectSerializer(project)
            watch_set = project.watch_set
            watchListseri = WatchSerializer(watch_set, many=True)

            #넘겨줄 유저정보를 여기에 추가한다.
            return JsonResponse(userSeri.data + projectSeri.data, safe=False)

        else :
            # 로그인 실패
            return JsonResponse({'result': 'fail'}, status=200)


#
# def CheckSTEMP(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         username = data['username']
#         password = data['password']
#
#         loginStatus = authenticate(username=username, password=password)
#         if loginStatus :
#             # 로그인 성공
#             museumID = data['QRData']
#             GPSstate = data['GPSstate']
#
#             #GPS가 맞는지 확인
#             StempTest = True
#
#             if StempTest:
#                 # user -> 박물관아이디로 -> 스탬프 정보 수정.
#
#             else:
#                 return JsonResponse({'result': 'GPS 지역 위반'}, status=200)
#
#          else:
#             # 로그인 실패
#             return JsonResponse({'result': '로그인 실패'}, status=200)
#






















# # def modityUser(request):
# #     #구현 필요
# #     if request.method == 'POST':
# #         data = JSONParser().parse(request)
# #
# #         user = User.objects.get(username='john')
# #         user.first_name = 'johnny'
# #         user.set_password('new password')  # 비밀번호 변경 함수
# #         user.save()