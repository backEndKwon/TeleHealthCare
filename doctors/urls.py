from rest_framework import routers
from django.urls import path, include
from . import views
from .views import DoctorViewSet

router = routers.DefaultRouter()

router.register('doctors', views.DoctorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', DoctorViewSet.as_view({'get':'searchDoctor'}), name='searchDoctor')
]