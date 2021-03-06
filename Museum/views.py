from django.shortcuts import render
#from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes  # JWT 데코레이터
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny   # 로그인 여부를 확인할 때 사용
from rest_framework_jwt.authentication import JSONWebTokenAuthentication    # JWT 인증을 확인하기 위해 사용
from django.contrib.auth.hashers import check_password
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import *
from .serializers import *
from django.contrib.auth.models import User     # 회원가입 필요

from haversine import haversine
import time
import json

# from django.contrib.auth import authenticate    # 아이디 비번 확인을 위해 사용
#from django.core.exceptions import ObjectDoesNotExist   # object 접근 에러처리



@api_view(['GET'])
@permission_classes((AllowAny, ))  #제한 없이 접근 가능
def HelloServer(request):
    if request.method == 'GET':
        return Response("hello Test!")


# @csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny, ))  #제한 없이 접근 가능
def MuseumData(request, pk):
    if request.method == 'GET':
        # data = JSONParser().parse(request)
        # museum_number = data['museum_number']
        try:
            museum = institution.objects.get(pk=pk)
        except institution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        serializer = institutionSerializer(museum)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # 박물관 정보를 설정하기 위한 기능이지만 관리자 페이지에서 할것이므로 비활성
    # if request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = MuseumSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)


@api_view(['PUT','POST'])
@permission_classes((AllowAny, ))  #제한 없이 접근 가능
def singUp(request):
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        username = data['username']
        try:
            # 중복 검사 실패
            user = User.objects.get(username=username)
        except:
            # 중복 검사 성공
            user = None
        if user is None:
            return Response("true",status=status.HTTP_200_OK)
        else:
            return Response("fail",status=status.HTTP_202_ACCEPTED)

    if request.method == 'POST':

        
        data = JSONParser().parse(request)
        if not data['appkey'] == '940109':
           return Response({'error': '앱키오류'}, status=status.HTTP_400_BAD_REQUEST)

        aim_key= data['joinkey']
        try:
            joinkey.objects.get(key=aim_key)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        username = data['username']
        password = data['password']
        re_password = data['re_password']
        email = data['email']
        first_name = data['first_name']
 

        if not(username and password and re_password and email and first_name) :
            return Response({'error': '빈칸'}, status=status.HTTP_400_BAD_REQUEST)
        elif password !=re_password:
            return Response({'error': '비번 다름'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(username=username)
            except:
                user = None
            if user is None:
                try:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name)
                    Watch_Student = Student(user=user)
                    Watch_Student.save()
                    for a in institution.objects.all():
                        w = Watch(Watch_Student=Watch_Student, Watch_institution=a)
                        w.save()
                except:
                    user.delete()
                    return Response({'message': '실패'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response("동일아이디 존재", status=status.HTTP_202_ACCEPTED)

            return Response({'message': '회원가입 완료'}, status=status.HTTP_201_CREATED)


# @csrf_exempt
@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def UserData(request):
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'GET':

        # data = JSONParser().parse(request)
        # username = data['username']
        # password = data['password']
        # loginStatus = authenticate(username=username, password=password)

        if user is not None:
            # 로그인 성공
            #userSeri = userSerializer(user)    # user 정보
            
            updateUser(user.student)
            userSeri = userCustomSerializer(user)  # user 정보
            return Response(userSeri.data, status=status.HTTP_200_OK)

        else :
            # 로그인 실패
            return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        now_password=data['password']
        if check_password(now_password,user.password):
            p1=data['new_password']
            p2=data['new_password_re']
            if p1==p2:
                user.set_password(p1)
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'error': '새로운 비밀번호 확인 실패'}, status=402)
        else:
                return Response({'error': '현재 비밀번호 확인 실패'}, status=status.HTTP_400_BAD_REQUEST)



# @csrf_exempt
@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def UserMuseumData(request, pk):
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'GET':
        # data = JSONParser().parse(request)
        # username = data['username']
        # password = data['password']
        # museum_number = data['museum_number']

        # loginStatus = authenticate(username=username, password=password)
        project = user.student
        watch_set = project.watch_set

        try:
            institution_obj = institution.objects.get(institution_number=pk)
            watch = watch_set.get(Watch_institution=institution_obj)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        watchListseri = WatchSerializer(watch)

        return Response(watchListseri.data,status=status.HTTP_200_OK)


    if request.method == 'PUT':
        data = JSONParser().parse(request)
        # username = data['username']
        # password = data['password']
        # museum_number = data['museum_number']
        try:

            quizAnswer = data['quizAnswer']
        except :
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # loginStatus = authenticate(username=username, password=password)

        # if loginStatus:
            # 로그인 성공
            # user = User.objects.get(username=username)

        project = user.student
        watch_set = project.watch_set
        try:
            institution_obj = institution.objects.get(institution_number=pk)
            watch = watch_set.get(Watch_institution=institution_obj)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            watch.quiz_answer = quizAnswer
            watch.save()

        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        watchListseri = WatchSerializer(watch)
        updateUser(project)
        return Response(watchListseri.data, status=status.HTTP_200_OK)
        # else :
        #     # 로그인 실패



# @csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def CheckSTEMP(request):
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'PUT':
        data_request = JSONParser().parse(request)
        request_gps = (float(data_request['latitude']), float(data_request['longitude']))  # 보낸 좌표
        aim_qrcode=data_request['QR']
        student =user.student
        watch_set = student.watch_set
        try:
            institution_obj = institution.objects.get(qrcode=aim_qrcode)
            watch = watch_set.get(Watch_institution=institution_obj)
            aim_gps = (float(institution_obj.latitude), float(institution_obj.longitude))  # 기관좌표
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if haversine(request_gps, aim_gps) < float(institution_obj.gps_error):  
            watch.stampStatus = True
            times=time.time()
            watch.create_Stamp_date=time.strftime('%a-%Y-%m-%d', time.localtime(times))
            watch.create_Stamp_time=time.strftime('%H:%M', time.localtime(times))
            watch.save()
            watchListseri = WatchSerializer(watch)
            updateUser(student)
            return Response(watchListseri.data, status=status.HTTP_200_OK)
        else:
            return Response({'result': 'GPS 지역 위반'}, status=status.HTTP_202_ACCEPTED)


# @csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def CheckSTEMP_staff(request):
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    if not user.is_staff:
        return Response(status=status.HTTP_401_UNAUTHORIZED)



    if request.method == 'PUT':
        data_request = JSONParser().parse(request)
        request_gps = (float(data_request['latitude']), float(data_request['longitude']))  # 보낸 좌표

        aim_institution_number=data_request['museumID']########
        aim_user=User.objects.get(username=data_request['student_id'])#####

        student =aim_user.student
        watch_set = student.watch_set
        try:

            institution_obj = institution.objects.get(institution_number=aim_institution_number)########

            watch = watch_set.get(Watch_institution=institution_obj)
            aim_gps = (float(institution_obj.latitude), float(institution_obj.longitude))  # 기관좌표
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if haversine(request_gps, aim_gps) < float(institution_obj.gps_error):  
            watch.stampStatus = True
            times=time.time()
            watch.create_Stamp_date=time.strftime('%a-%Y-%m-%d', time.localtime(times))
            watch.create_Stamp_time=time.strftime('%H:%M', time.localtime(times))
            watch.save()
            watchListseri = WatchSerializer(watch)
            updateUser(student)
            return Response(watchListseri.data, status=status.HTTP_200_OK)
        else:
            return Response({'result': 'GPS 지역 위반'}, status=status.HTTP_202_ACCEPTED)


@api_view(['PUT','GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def feeling(request):
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'PUT':
        data_request = JSONParser().parse(request)
        feel = data_request['feel']
        if len(feel)<30:
            return Response(status=202)
        student =user.student

        try:
            student.feeling=feel
            student.save()
            updateUser(student)
            return Response({'feel': student.feeling}, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=404)


    elif request.method == 'GET':
        try:
            student = user.student
            return Response({'feel': student.feeling}, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=404)


def updateUser(student):
    watchset = student.watch_set
    if len( student.feeling) < 30:
        return False
    standardStrLen = 15
    for w in watchset.all():

        if len(w.quiz_answer) < standardStrLen or not w.stampStatus:
            student.CompleteState = False
            return False
    student.CompleteState = True
    student.save()
    return True



@api_view(['GET','DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def Community_get_del(request, pk):  
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'GET':
        page=pk
        query_set = Community.objects.all()[(page - 1) * 20:]  # page번째 글 찾음
        if query_set.count() >= 20:  # 20개이상 글있으면 20개 글반환
            query_set = query_set[:20]
        serializer = CommunitySerializer(query_set, many=True)
        for x in serializer.data:
            if x['author'] != str(user):
                obj=str(x['author'])
                obj=obj[:len(obj)-3]+'***'
                x['author']=obj
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':  # DELETE면 삭제
        user = None
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            obj = Community.objects.get(id=str(pk))  # 수정 혹은 삭제 될 데이터
        except Exception:
            return Response(status=401)
      
        if obj.author ==username:
            obj.delete()
            return Response(status=204)
        return Response(status=400)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def Community_post(request): 
    if request.method == 'POST':
        user = None
        username = request.user.username
        user = User.objects.get(username=username)
        data = JSONParser().parse(request)
        obj=Community.objects.create(author=username,text=data['text'])
        obj.save
        return Response(status=status.HTTP_201_CREATED)

def check_quiz(watch):
    if len(watch.quiz_answer) > 15:
        return True
    else:
        return False

def check_stamp(watch):
    if watch.stampStatus:
        return True
    else:
        return False

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def stampstatus(request):
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    student =user.student
    updateUser(student)
    if request.method == 'GET':
        watchset = student.watch_set.all()
        try:
            lst=[]
            for muse in watchset:
                name=muse.Watch_institution.institution_number
                stamp=check_stamp(muse)
                quiz=check_quiz(muse)
                lst.append({'museum':name,'quiz':quiz, 'stamp':stamp})
        except Exception:
            return Response(status=404)


        feeling=None
        if len(student.feeling)>30:
            feeling=True
        else:
            feeling=False
        CompleteState=student.CompleteState
        lst.append({'feeling':feeling,'CompleteState':CompleteState})



        return Response(lst,
                         status=status.HTTP_200_OK)











