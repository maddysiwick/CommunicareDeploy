from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import DoctorProfile,PatientProfile,User

