from django.shortcuts import render
from .models import Doctor
from rest_framework import viewsets
from .serializers import DoctorSerializer

# Create your views here.

class doctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer