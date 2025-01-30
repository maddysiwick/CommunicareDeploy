from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractUser

# Create your models here.
#DONT MIGRATE ANYTHINGUNTIL YOU HAVE THE DB SET UP
    
class User(AbstractUser):
    is_doctor=models.BooleanField(default=False)
    is_patient=models.BooleanField(default=False)
    name=models.CharField(max_length=100)
    acessibility=models.BooleanField(default=False)
    location=models.PointField(default=Point(0,0))

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    is_male=models.BooleanField(default=False)
    is_female=models.BooleanField(defaut=False)
    specialty=models.CharField(max_length=100)

class PatientProfile(models.model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)