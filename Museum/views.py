from django.shortcuts import render
#from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes  # JWT 데코레이터
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny   # 로그인 여부를 확인할 때 사용
from rest_framework_jwt.authentication import JSONWebTokenAuthentication    # JWT 인증을 확인하기 위해 사용

# from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import *
from .serializers import *

from django.contrib.auth.models import User     # 회원가입 필요
# from django.contrib.auth import authenticate    # 아이디 비번 확인을 위해 사용

#from django.core.exceptions import ObjectDoesNotExist   # object 접근 에러처리


# Create your views here.

# @api_view(['GET','POST'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))


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


@api_view(['GET','POST'])
@permission_classes((AllowAny, ))  #제한 없이 접근 가능
def singUp(request):
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
            return Response("true",status=status.HTTP_200_OK)
        else:
            return Response("fail",status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        username = data['username']
        password = data['password']
        re_password = data['re_password']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']

        if not(username and password and re_password and email and first_name and last_name) :
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
                                                    first_name=first_name, last_name=last_name)
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
@api_view(['GET'])
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
            userSeri = userCustomSerializer(user)  # user 정보
            return Response(userSeri.data, status=status.HTTP_200_OK)

        else :
            # 로그인 실패
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 구현 필요 회원 정보 수정 및 비밀번호 변경
    # if request.method == 'PUT':
    #     data = JSONParser().parse(request)
    #
    #     user = User.objects.get(username='john')
    #     user.first_name = 'johnny'
    #     user.set_password('new password')  # 비밀번호 변경 함수
    #     user.save()



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

            quizNumber = data['quizNumber']
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

        if (quizNumber == '1'):
            watch.quiz1_answer = quizAnswer
            watch.save()
        elif (quizNumber == '2'):
            watch.quiz2_answer = quizAnswer
            watch.save()
        elif (quizNumber == '3'):
            watch.quiz3_answer = quizAnswer
            watch.save()
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        watchListseri = WatchSerializer(watch)
        updateUser(project)
        return Response(watchListseri.data, status=status.HTTP_200_OK)
        # else :
        #     # 로그인 실패



# @csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def CheckSTEMP(request, pk):
    user = None
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # username = data['username']
        # password = data['password']
        # museumID = data['QRData']
        GPSstate = data['GPSstate']

        # loginStatus = authenticate(username=username, password=password)
        # if loginStatus :
            #user = User.objects.get(username=username)

        project = user.student
        watch_set = project.watch_set
        try:
            institution_obj = institution.objects.get(institution_number=pk)
            watch = watch_set.get(Watch_institution=institution_obj)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #===========test===================
        # GPS가 맞는지 확인
        StempTest = True  # test 무조건 맞다.
        #=============test=================

        if StempTest:   # 조건에 맞다고하면
            watch.stampStatus = True
            watch.save()
            watchListseri = WatchSerializer(watch)
            updateUser(project)
            return Response(watchListseri.data, status=status.HTTP_200_OK)
        else:
            return Response({'result': 'GPS 지역 위반'}, status=status.HTTP_202_ACCEPTED)
        # else:
        #     # 로그인 실패
        #     return JsonResponse({'result': '로그인 실패'}, status=200)



def updateUser(student):
    watchset = student.watch_set
    standardStrLen = 10
    for w in watchset.all():

        if len(w.quiz1_answer) < standardStrLen or len(w.quiz2_answer) < standardStrLen or len(
                w.quiz3_answer) < standardStrLen or not w.stampStatus:
            student.CompleteState = False
            return False
    student.CompleteState = True
    student.save()
    return True


@csrf_exempt
def Community_page(request, page):  # 5개씩페이지 page값 url로 받아오기
    if request.method == 'GET':
        query_set = Community.objects.all()[(page - 1) * 5:]  # page번째 글 찾음
        if query_set.count() >= 5:  # 5개이상 글있으면 5개 글반환
            query_set = query_set[:5]
        serializer = CommunitySerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def Community_object(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommunitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def Community_ud(request, id):  # 수정 혹은 삭제할 때는 id url로
    obj = Community.objects.get(pk=id)  # 수정 혹은 삭제 될 데이터
    if request.method == 'PUT':  # PUT이면 수정
        data = JSONParser().parse(request)
        serializer = CommunitySerializer(obj, data=data)  # 수정 obj도 넣어줌
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':  # DELETE면 삭제
        obj.delete()
        return HttpResponse(status=204)


@csrf_exempt
def random_key(request):  # 테스트 안해봄, 추가적으로 더구현해야함, 일단보류하기로함
    if request.method == 'GET':
        while (True):
            rand = randint(1000, 10000)
            query_set = rand_key.objects.filter(key=rand)
            if len(query_set) > 0:
                rand_key.objects.create(key=rand)
                break
        data = rand_key.objects.get(key=rand)
        serializer = rand_keySerializer(data=data)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def stamp(request):  # id,institution_number,latitude, longitude 4가지 받아야함
    if request.method == 'PUT':
        data_request = JSONParser().parse(request)
        request_institution = data_request['institution_number']  # 보낸 기관번호
        request_gps = (float(data_request['latitude']), float(data_request['longitude']))  # 보낸 좌표
        try:
            query_set = institution.objects.get(institution_number=request_institution)
            aim_gps = (float(query_set.latitude), float(query_set.longitude))  # 기관좌표
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if haversine(request_gps, aim_gps) < 0.5:  # 거리가 0.5km이하면
            try:
                obj = Watch.objects.get(Watch_Student__user__username=data_request['id'],
                                        Watch_institution__institution_number=request_institution)
                obj.stampStatus = True
                obj.save()
            except Exception:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return HttpResponse(status=204)



