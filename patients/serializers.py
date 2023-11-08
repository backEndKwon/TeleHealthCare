# 장고 모델 데이터를 json타입으로 바꿔주는 작업 = 직렬화 작업
# 작업 이유 => json으로 바꿔줘야 api로 데이터를 전송할 수 있으니까

from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__' #모든 필드를 직렬화 해줘라
        #fields = ['patientId', 'name'] #특정 필드만 직렬화 해줘라

