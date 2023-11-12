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

    # #시간을 24시간 형식으로 변환
    # #ex) 1시 -> 13, 2시 -> 14, 3시 -> 15, 4시 -> 16, 5시 -> 17, 6시 -> 18, 7시 -> 19, 8시 -> 20, 9시 -> 21, 10시 -> 22, 11시 -> 23, 12시 -> 24
    # def convertTimeFormat(self, time):
    #     time = time.replace('시', '')
    #     if '오후' in time:
    #         hour = int(time.replace('오후', '').strip()) + 12
    #     else:
    #         hour = int(time.replace('오전', '').strip())
    #     return hour

    # #입력한 시간이 의사의 영업시간 내에 있는지 확인
    # def isWithinWorkingHours(self, user_time, working_hours, lunch_hours):
    #     if '휴무' in working_hours:
    #         return False
    #     #~로 구분된 시간을 24시간 형식으로 변환
    #     working_start, working_end = [int(self.convertTimeFormat(t)) for t in working_hours.split('~')]
    #     lunch_start, lunch_end = [int(self.convertTimeFormat(t)) for t in lunch_hours.split('~')]
    #     # 유효한 시간 : 일하는 시간 <= 신청한 시간 < 점심시간 또는 점심시간 <= 신청한 시간 < 일하는 시간
    #     return (working_start <= user_time < lunch_start or lunch_end <= user_time < working_end)

    #nestjs의 @Query()와 같은 기능 + controller에서 사용할 수 있도록 @action 데코레이터 사용
    @action(detail=False, methods=['GET'])
    def searchDoctor(self, request):
        keyword = request.query_params.get('keyword', None)
        datetime_str = request.query_params.get('datetime', None)

        #만약 keyword가 존재하면 keyword에 해당하는 의사를 찾아서 반환
        if keyword is not None:
            doctors = Doctor.objects.filter(Q(department__icontains=keyword) | Q(department_selfPay__icontains=keyword) | Q(hospital__icontains=keyword))
            #keyword에 해당하는 의사가 없으면 에러 메시지 반환
            if not doctors.exists():
                return Response({"message": "키워드에 해당하는 의사를 찾을 수 없습니다. 다시 입력하세요."})
        
        #datetime_str에 해당하는 의사를 찾아서 반환
        elif datetime_str is not None:
            datetime_str = datetime_str.replace('년 ', '-').replace('월 ', '-').replace('일 ', ' ')
            try:
                hour = int(convertTimeFormat(datetime_str.split(' ')[1]))
            except ValueError:
                return Response({"message": "올바른 시간 형식을 입력해주세요."})
            
            datetime_str = datetime_str.replace(datetime_str.split(' ')[1], str(hour))

            try:
                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H')
            except ValueError:
                return Response({"message": "올바른 날짜 형식을 입력해주세요."})

            weekday = datetime_obj.weekday() 
            print("weekday: ", weekday)
            user_time = datetime_obj.time().hour

            doctors = Doctor.objects.all()
            available_doctors = [doctor for doctor in doctors if isWithinWorkingHours_doctor(user_time, doctor.time_business.split('/')[weekday], doctor.time_lunch)]
            print("available_doctors: ", available_doctors)
            
            if not available_doctors:
                return Response({"message": "입력한 시간에 영업 중인 의사를 찾을 수 없습니다."})

            serializer = self.get_serializer(available_doctors, many=True)
            doctor_names = [doctor['name'] for doctor in serializer.data]
            return Response(doctor_names)
        else:
            doctors = Doctor.objects.all()

        serializer = self.get_serializer(doctors, many=True)
        doctor_names = [doctor['name'] for doctor in serializer.data]
        return Response(doctor_names)