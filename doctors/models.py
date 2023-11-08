from django.db import models
import uuid
#ArrayField를 사용하기 위해 import
from django.contrib.postgres.fields import ArrayField
#model, entity와 같은 역할
# Create your models here.
    
class Doctor(models.Model):
    #doctorId, hospital(병원명), doctorName(의사명)
    #department(진료과, 여러개 입력가능), selfPayDepartment(비급여진료과, 여러개 입력가능)
    # 시간 입력방식
    #영업시간란 : 월~금:오전9시~오후7시, 토:오전9시~오후1시
    #점심시간란 : 월~금:오후1시~오후2시
    #휴무일 :일,공휴일
    #businessTime(영업시간)
    #lunchTime(점심시간)
    #holidayTime(휴무일)
    
    doctorId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.CharField(max_length=50, null=False,blank=False)
    doctorName = models.CharField(max_length=17, null=False,blank=False)
    department = models.TextField(null=False,blank=False)
    department_selfPay = models.TextField(null=False,blank=False)
    #사용자에게 입력받는 방식 :
    #첫번째 칸 부터 월~일 이라는 가정하에 입력받음
    #구분은 쉼표
    #ex) 오전9시~오후5시/오전9시~오후5시/오전9시~오후5시/오전9시~오후5시/오전9시~오후5시/오전9시~오후1시/휴무
    time_business = models.TextField(null=False,blank=False)
    #일단 공휴일은 고려하지 않는다.
    
    #사용자에게 입력받는 방식 :
    #오전12시~오후1시
    time_lunch = models.TextField(null=False,blank=False)


#추후 선택박스로 구현할 수 있게 되면 월~일을 0~6으로 바꿔서 구현하기
