from django.shortcuts import render
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer
#modelviewset은 crud를 모두 지원해줌
# 모델명.objects.all() => 모델명에 해당하는 모든 데이터를 가져옴
#serializer_class = patientSerializer 를 사용하겠다는 의미
# Create your views here.
class patientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer