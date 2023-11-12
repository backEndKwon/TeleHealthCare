# 받아온 데이터를 JSON 형식으로 변환해주는 역할
from rest_framework import serializers
from .models import Treatment

#nestjs의 dto와 비슷한 역할
class TreatmentSerializer(serializers.ModelSerializer):
    patientName = serializers.CharField(source='patient.name', read_only=True)
    doctorName = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = Treatment
        
        #return 값 형식 지정
        fields = ['treatmentId', 'patientName', 'doctorName', 'rezDate', 'rezExpirationDate', 'isAccepted']
        read_only_fields = ['rezExpirationDate', 'isAccepted', 'createdAt']  