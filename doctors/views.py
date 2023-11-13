from django.shortcuts import render
from .models import Doctor
from rest_framework import viewsets
from .serializers import DoctorSerializer
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from datetime import datetime
from teleHealthCare.utils import isWithinWorkingHours_doctor, convertTimeFormat
# Create your views here.

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    
    @action(detail=False, methods=['GET'])
    def searchDoctor(self, request):
        keyword = request.query_params.get('keyword', None)
        datetimeStr = request.query_params.get('datetime', None)

        #만약 keyword가 존재하면 keyword에 해당하는 의사를 찾아서 반환
        if keyword is not None:
            doctors = Doctor.objects.filter(Q(department__icontains=keyword) | Q(department_selfPay__icontains=keyword) | Q(hospital__icontains=keyword))
            #keyword에 해당하는 의사가 없으면 에러 메시지 반환
            if not doctors.exists():
                return Response({"message": "키워드에 해당하는 의사를 찾을 수 없습니다. 다시 입력하세요."})
        
        #datetime_str에 해당하는 의사를 찾아서 반환
        elif datetimeStr is not None:
            datetimeStr = datetimeStr.replace('년 ', '-').replace('월 ', '-').replace('일 ', ' ')
            try:
                hour = int(convertTimeFormat(datetimeStr.split(' ')[1]))
            except ValueError:
                return Response({"message": "올바른 시간 형식을 입력해주세요."})
            
            datetimeStr = datetimeStr.replace(datetimeStr.split(' ')[1], str(hour))

            try:
                datetimeObj = datetime.strptime(datetimeStr, '%Y-%m-%d %H')
            except ValueError:
                return Response({"message": "올바른 날짜 형식을 입력해주세요."})

            weekday = datetimeObj.weekday() 
            userTime = datetimeObj.time().hour

            doctors = Doctor.objects.all()
            if not doctors: #의사 정보 없으면 에러메세지 반환
                return Response({"message": "검색 결과가 없습니다."})

            availableDoctors = [doctor for doctor in doctors if isWithinWorkingHours_doctor(userTime, doctor.time_business.split('/')[weekday], doctor.time_lunch)]
            if not availableDoctors:
                return Response({"message": "입력한 시간에 영업 중인 의사를 찾을 수 없습니다."})

            serializer = self.get_serializer(availableDoctors, many=True)
            doctorNames = [doctor['name'] for doctor in serializer.data]
            return Response(doctorNames)
        else:
            doctors = Doctor.objects.all()

        serializer = self.get_serializer(doctors, many=True)
        doctorNames = [doctor['name'] for doctor in serializer.data]
        return Response(doctorNames)