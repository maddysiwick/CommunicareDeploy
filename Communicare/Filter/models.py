from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# Create your models here.

class Doctor(models.Model):
    name=models.CharField(max_length=100)
    specialty=models.CharField(max_length=100)
    accessibility=models.BooleanField(default=True)
    sex=models.BooleanField(default=True) #probably shouldnt be a bool idk check before migrating
    location=models.PointField(defauly=Point(0,0))

    def __str__(self):
        return self.name