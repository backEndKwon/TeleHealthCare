from django.shortcuts import render
from .models import Doctor
from rest_framework import viewsets
from .serializers import DoctorSerializer
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from datetime import datetime
# Create your views here.

class doctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    
    @action(detail=False, methods=['GET'])
    def searchDoctor(self, request):
        keyword = request.query_params.get('keyword', None)
        
        if keyword is not None:
            doctors = Doctor.objects.filter(Q(doctorName__icontains=keyword) | Q(department_selfPay__icontains=keyword) | Q(hospital__icontains=keyword))
            if not doctors.exists():
                return Response({"키워드에 해당하는 의사를 찾을 수 없습니다. 다시 입력하세요."})
        else:
            doctors = Doctor.objects.all()
        
        serializer = self.get_serializer(doctors, many=True)
        doctor_names = [doctor['doctorName'] for doctor in serializer.data]
        return Response(doctor_names)