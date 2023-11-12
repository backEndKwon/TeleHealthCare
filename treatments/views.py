from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Treatment
from .serializers import TreatmentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from teleHealthCare.utils import isWithinWorkingHours, convertTimeFormat, calculateExpirationDate, parseDateString
from doctors.models import Doctor
from patients.models import Patient

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    @action(detail=False, methods=['POST'])
    def createTreatment(self, request):
        print("---------------확인용--------------")
        # 1. 요청으로부터 데이터를 추출
        patientId = request.data.get('patientId')
        doctorId = request.data.get('doctorId')
        rez_date_str = request.data.get('rezDate')

        # 2. `patient`와 `doctor` 객체를 DB에서 가져옴
        patient = Patient.objects.filter(pk=patientId).first()
        doctor = Doctor.objects.filter(pk=doctorId).first()

        # 3. `patient`나 `doctor`가 존재하지 않을 경우 에러 메시지를 반환
        if not patient or not doctor:
            return Response({'message': 'patientId나 doctorId가 존재하지 않습니다.'})

        # 4. `rez_date_str`을 datetime 객체로 변환
        rez_date = parseDateString(rez_date_str)
        
        # 5. 진료 요청 시간이 의사의 근무 시간 내에 있는지 확인
        rez_date_check = isWithinWorkingHours(rez_date.time().hour, doctor.time_business.split('/')[rez_date.weekday()], doctor.time_lunch)
        
        current_time = datetime.now()

        if isinstance(rez_date_check, str):
            # 7. 새로운 `Treatment` 객체를 생성
            treatment = Treatment.objects.create(patient=patient, doctor=doctor, rezDate=rez_date_check, rezExpirationDate=calculateExpirationDate(current_time, doctor).strftime('%Y-%m-%d %H:%M:%S'))
            treatment.isAccepted = False

            # 8. `Treatment` 객체를 DB에 저장
            treatment.save()

            # 9. `Treatment` 객체를 직렬화하여 응답 데이터를 생성
            serializer = self.get_serializer(treatment)
            return Response(serializer.data)
        
        # 6. 진료 요청 만료 날짜와 시간을 계산
        rez_expiration_date = calculateExpirationDate(current_time, doctor)

        # 7. 새로운 `Treatment` 객체를 생성
        treatment = Treatment.objects.create(patient=patient, doctor=doctor, rezDate=rez_date.strftime('%Y년 %m월 %d일 %H시%M분'), rezExpirationDate=rez_expiration_date.strftime('%Y-%m-%d %H:%M:%S'))
        treatment.isAccepted = False

        # 8. `Treatment` 객체를 DB에 저장
        treatment.save()

        # 9. `Treatment` 객체를 직렬화하여 응답 데이터를 생성
        serializer = self.get_serializer(treatment)
        return Response(serializer.data)