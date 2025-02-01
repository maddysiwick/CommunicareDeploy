from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.gis.geos import Point

from .models import DoctorProfile,PatientProfile,User,Language

class PatientSignupForm(UserCreationForm):
    languages=forms.MultipleChoiceField(choices=Language.objects.all(),required=True,help_text='what languages do you speak')
    name=forms.CharField(max_length=100,help_text='what is your name')
    accessibility=forms.BooleanField(help_text='do you need the office to be acessible')
    #NEED TO FIX THIS IN THE FUTUR CANT BE ASKING USERS FOR COORDINATES
    lat=forms.FloatField(help_text='please input your lat coordinate')
    long=forms.FloatField(help_text='please input your long coordinate')

    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_patient=True
        user.languages.add(*self.cleaned_data.get('languages'))
        lat=self.cleaned_data.get('lat')
        long=self.cleaned_data.get('long')
        user.location=Point(long,lat)
        user.accessibility=self.cleaned_data.get('accessibility')
        user.save()
        patient=PatientProfile.objects.create(user=user)
        return user
    

class DoctorSignupForm(UserCreationForm):
    languages=forms.MultipleChoiceField(choices=Language.objects.all(),required=True,help_text='what languages do you speak')
    name=forms.CharField(max_length=100,help_text='what is your name')
    accessibility=forms.BooleanField(help_text='is your office accessible')
    #NEED TO FIX THIS IN THE FUTUR CANT BE ASKING USERS FOR COORDINATES
    lat=forms.FloatField(help_text='please input your lat coordinate')
    long=forms.FloatField(help_text='please input your long coordinate')
    male=forms.BooleanField(help_text='m')
    female=forms.BooleanField(help_text='f')

    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_doctor=True
        user.languages.add(*self.cleaned_data.get('languages'))
        lat=self.cleaned_data.get('lat')
        long=self.cleaned_data.get('long')
        user.location=Point(long,lat)
        user.accessibility=self.cleaned_data.get('accessibility')
        user.save()
        doc=DoctorProfile.objects.create(user=user)
        doc.is_female=self.cleaned_data.get('female')
        doc.is_male=self.cleaned_data.get('male')
        return user