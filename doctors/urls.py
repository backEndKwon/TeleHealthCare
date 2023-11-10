from rest_framework import routers
from django.urls import path, include
from . import views
from .views import doctorViewSet

router = routers.DefaultRouter()

router.register('doctors', views.doctorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', doctorViewSet.as_view({'get':'searchDoctor'}), name='searchDoctor')
]