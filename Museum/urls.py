
from django.urls import path
from .views import *

urlpatterns = [
    path('test/', HelloServer),     # 서버 상태 체크
    path('museum/<str:pk>/', MuseumData),   # 박물관 정보 받기 1~n 박물관 개수 admin site 확인 필요
    path('singUp/', singUp),    # 회원가입만 진행 -> 사용을 위한 토큰은 따로 발급하도록 진행.

    path('login/', UserData),   #
    path('usermuseum/<str:pk>/', UserMuseumData),
    path('stemp/', CheckSTEMP),
    path('stemp_staff/', CheckSTEMP_staff),
    path('feel/', feeling),
    path('comu/', Community_object),# 글생성
    path('comupage/', Community_page), #page당 5개씩 글 데이터 전송
    path('comuud/', Community_ud), #글 수정 및 삭제
]
