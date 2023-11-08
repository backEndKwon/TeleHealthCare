from rest_framework import serializers
from .models import Doctor

#직렬화 작업(Django model -> JSON)
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__' #모든 필드를 직렬화 해줘라