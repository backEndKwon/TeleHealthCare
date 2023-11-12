from django.db import models
from patients.models import Patient
from doctors.models import Doctor
import uuid
from django.utils import timezone
# Create your models here.

class Treatment(models.Model):
    treatmentId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    #환자와 의사의 id foreign key로 연결
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
    
    #rez= reservation
    #진료희망날짜&시간과 진료요청 만료날짜&시간
    rezDate = models.CharField(max_length=50)
    rezExpirationDate = models.CharField(max_length=50)
    
    #진료예약 승인여부
    isAccepted = models.BooleanField(default=False)
    
    #진료요청이 발행된 date
    createdAt = models.DateTimeField(default=timezone.now)