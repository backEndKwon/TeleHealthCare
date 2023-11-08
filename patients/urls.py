#router 등록
from rest_framework import routers
from django.urls import include, path
from . import views
#-> views.py를 import한 것 =>왜? views.patientViewSet를 router에 등록하기 위해

#default router 설정
router = routers.DefaultRouter()

router.register('patients',views.patientViewSet) #두개 인자 모두 router에 등록

urlpatterns =[
    path('',include(router.urls))
]