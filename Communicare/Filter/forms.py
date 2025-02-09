from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
#from django.contrib.gis.geos import Point

from .models import DoctorProfile,User,Language

class PatientSignupForm(UserCreationForm):
    languages=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Language.objects.all(),required=True,help_text='what languages do you speak')
    
    name=forms.CharField(max_length=100,help_text='what is your name')
    accessibility=forms.BooleanField(help_text='do you need the office to be acessible',required=False)
    #NEED TO FIX THIS IN THE FUTUR CANT BE ASKING USERS FOR COORDINATES
    lat=forms.FloatField(help_text='please input your lat coordinate')
    long=forms.FloatField(help_text='please input your long coordinate')

    class Meta(UserCreationForm.Meta):
        model=User
        fields = ['languages', 'name', 'accessibility', 'lat', 'long']

    widgets = {
        'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'This is your name'}),
        'lat': forms.TextInput(attrs={'class':'form-control'}),
        'long': forms.TextInput(attrs={'class':'form-control'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_class = 'label-red'

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_patient=True
        user.save()
        user.languages.add(*self.cleaned_data.get('languages'))
        lat=self.cleaned_data.get('lat')
        long=self.cleaned_data.get('long')
        #user.location=Point(long,lat)
        user.accessibility=self.cleaned_data.get('accessibility')
        user.save()
        return user
    
    
    


class DoctorSignupForm(UserCreationForm):
    languages=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Language.objects.all(),required=True,help_text='what languages do you speak')
    name=forms.CharField(max_length=100,help_text='what is your name')
    accessibility=forms.BooleanField(help_text='is your office accessible',required=False)
    #NEED TO FIX THIS IN THE FUTUR CANT BE ASKING USERS FOR COORDINATES
    lat=forms.FloatField(help_text='please input your lat coordinate')
    long=forms.FloatField(help_text='please input your long coordinate')
    male=forms.BooleanField(help_text='m',required=False)
    female=forms.BooleanField(help_text='f',required=False)
    specialty=forms.CharField(help_text='what is your field of specialty')

    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_doctor=True
        user.name=self.cleaned_data.get('name')
        user.acessibility=self.cleaned_data.get('accessibility')
        user.save()
        user.languages.add(*self.cleaned_data.get('languages'))
        lat=self.cleaned_data.get('lat')
        long=self.cleaned_data.get('long')
        #user.location=Point(long,lat)
        user.accessibility=self.cleaned_data.get('accessibility')
        doc=DoctorProfile.objects.create()
        doc.is_female=self.cleaned_data.get('female')
        doc.is_male=self.cleaned_data.get('male')
        doc.specialty=self.cleaned_data.get('specialty')
        doc.save()
        user.profile=doc
        user.save()
        return user

class SearchCrieteriaForm(forms.Form):
    distance=forms.IntegerField(help_text='what is the max distNCE YOU ARE WILLING TO TRAVEL(m)')
    #replace this with a multiple choice field at some point
    specialty=forms.CharField(help_text='what kimd of professional are you looking for')
    male=forms.BooleanField(help_text='i need a male doctor',required=False)
    female=forms.BooleanField(help_text='i need a female docgtor',required=False)
