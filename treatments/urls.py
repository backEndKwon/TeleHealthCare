from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreatmentViewSet
from . import views

router = DefaultRouter()
router.register('treatments', views.TreatmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]