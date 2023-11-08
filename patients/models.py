from django.db import models
import uuid

# Create your models here.
class Patient(models.Model):
    patientId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=17) ##국내 제일 긴 이름 17자 