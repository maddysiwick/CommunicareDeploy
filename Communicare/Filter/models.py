from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Language(models.Model):
    lang=models.CharField(max_length=100)

    def __str__(self):
        return self.lang

 
class User(AbstractUser):
    is_doctor=models.BooleanField(default=False)
    is_patient=models.BooleanField(default=False)
    name=models.CharField(max_length=100)
    acessibility=models.BooleanField(default=False)
    address=models.CharField(max_length=500,null=True)
    location=models.PointField(null=True,blank=True)
    languages=models.ManyToManyField(Language)
    asylum=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='docprofile',null=True)
    is_male=models.BooleanField(default=False)
    is_female=models.BooleanField(default=False)
    specialty=models.CharField(max_length=100)

class PatientProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='patientprofile',null=True)
    providers=models.ManyToManyField(User,related_name='patients',blank=True)

class Image(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    def __str(self):
        return self.name