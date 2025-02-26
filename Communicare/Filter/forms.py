from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.gis.geos import Point
from geopy import Nominatim
from dal import autocomplete
from .models import DoctorProfile,User,Language,PatientProfile

def getCoords(addressBad):
    geolocator=Nominatim(user_agent='Communicare')
    location=geolocator.geocode(addressBad)
    address=location.address
    point=Point(location.longitude,location.latitude)
    return [address,point]


class PatientSignupForm(UserCreationForm):
    languages=forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=autocomplete.Select2Multiple(url='language-autocomplete',attrs={'multiple':True}))
        
        
    
    name=forms.CharField(max_length=100)#help_text='what is your name')
    accessibility=forms.BooleanField(help_text='I am physically handicapped',required=False)
    address=forms.CharField(max_length=500)
    asylum=forms.BooleanField(required=False)
    class Meta(UserCreationForm.Meta):
        model=User
        #fields = ['languages', 'name', 'accessibility', 'address']

    widgets = {
        'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'This is your name'}),
        'address': forms.TextInput(attrs={'class':'form-control'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password2' in self.fields:
            self.fields['password2'].help_text = None
        for field in self.fields.values():
            field.label_class = 'label-red'

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_patient=True
        user.save()
        user.languages.add(*self.cleaned_data.get('languages'))
        spacial=getCoords(self.cleaned_data.get('address'))
        user.address=spacial[0]
        user.location=spacial[1]
        user.accessibility=self.cleaned_data.get('accessibility')
        user.asylum=self.cleaned_data.get('asylum')
        user.save()
        pat=PatientProfile.objects.create()
        pat.user=user
        pat.save()
        user.save()
        return user
    
    
    


class DoctorSignupForm(UserCreationForm):
    languages=forms.ModelMultipleChoiceField(widget=autocomplete.Select2Multiple(url='language-autocomplete',attrs={'multiple':True}),queryset=Language.objects.all(),required=True,help_text='what languages do you speak')
    name=forms.CharField(max_length=100)
    accessibility=forms.BooleanField(help_text='My office is accessible to people with physical handicaps',required=False)
    address=forms.CharField(max_length=500)
    male=forms.BooleanField(help_text='m',required=False)
    female=forms.BooleanField(help_text='f',required=False)
    asylum=forms.BooleanField(required=False)
    
    specialty=forms.CharField(help_text='what is your field of specialty')

    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_doctor=True
        user.name=self.cleaned_data.get('name')
        user.acessibility=self.cleaned_data.get('accessibility')
        user.asylum=self.cleaned_data.get('asylum')
        user.save()
        user.languages.add(*self.cleaned_data.get('languages'))
        spacial=getCoords(self.cleaned_data.get('address'))
        print(spacial[0])
        user.address=spacial[0]
        user.location=spacial[1]
        user.accessibility=self.cleaned_data.get('accessibility')
        doc=DoctorProfile.objects.create()

        doc.is_female=self.cleaned_data.get('female')
        doc.is_male=self.cleaned_data.get('male')
    
        doc.specialty=self.cleaned_data.get('specialty')
        doc.user=user
        doc.save()
        user.save()
        return user

class SearchCrieteriaForm(forms.Form):
    distance=forms.IntegerField()
    #replace this with a multiple choice field at some point
    specialty=forms.CharField()
    male=forms.BooleanField(help_text="I would prefer a male healthcare provider",required=False,  widget=forms.CheckboxInput(attrs={'aria-label': 'Male'}))
    female=forms.BooleanField(help_text="I would prefer a female healthcare provider",required=False,  widget=forms.CheckboxInput(attrs={'aria-label': 'Female'}))
    
   
class loginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)