from django.contrib.auth import login,authenticate
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from .models import User,DoctorProfile
from .forms import DoctorSignupForm,PatientSignupForm,SearchCrieteriaForm,loginForm
#from django.contrib.gis.measure import Distance
#from django.contrib.gis.geos import Point
from django.db.models import Q
from django.views.generic.edit import FormView
from django.views import View
from .models import Language
from django import forms
from dal import autocomplete
import os
from django.conf import settings
from .makelangs import langs

# Create your views here.
#these views might be ass go back over them later

class languageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs=Language.objects.all()
        if self.q:
            qs=qs.filter(lang__contains=self.q)
        return qs
    def get_result_label(self,item):
        return item.lang

class DocSignupView(CreateView):
    model=User
    form_class=DoctorSignupForm
    template_name='signupForm.html'
    languages = Language.objects.all

    def get_context_data(self, **kwargs):
        kwargs['user_type']='doctor'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect('home')
    

class PatientSignupView(CreateView):
    model=User
    form_class=PatientSignupForm
    template_name='signupForm.html'
    languages = Language.objects.all
    

    def get_context_data(self, **kwargs):
        kwargs['user_type']='patient'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user=form.save()
        selected_languages = form.cleaned_data['languages']
        user.languages.set(selected_languages)
        login(self.request,user)
        return redirect('home')
    
def home(request):
    langs.populate()
    return render(request,'home.html')

def triage(request):
    return render(request,'triage.html')

class searchCriteria(FormView):
    template_name='searchCriteria.html'
    form_class=SearchCrieteriaForm

    def form_valid(self,form):
        #MAJOR CHEAT FIX THIS
        #distance=((form.cleaned_data.get('distance'))/40075.017)*360
        specialty=form.cleaned_data.get('specialty')
        female=form.cleaned_data.get('female')
        male=form.cleaned_data.get('male')
        #print(distance)
        print(specialty)
        print(female)
        print(male)
        return redirect('searchresults',specialty,female,male)
    def form_invalid(self, form):
        return redirect('home')


class searchResults(View):
    def get(self,request,specialty,female,male):
        me=request.user
        #here=me.location
        languages=me.languages.all()
        accessibility=me.acessibility
        asylum=me.asylum
        doctors=[]
        #&Q(location__within=here.buffer(float(distance)))
        query=Q(is_doctor=True)&Q(docprofile__specialty=specialty)
        print(me.location)
        if accessibility==True:
            query&=Q(accessibility=True)
        if male==True:
            query&=Q(is_male=True)
        if female==True:
            query&=Q(is_female=True)
        if asylum==True:
            query&=Q(asylum=True)
        for language in languages:
            doctors+=language.user_set.filter(query)
        print(len(doctors))
        doctors=list(set(doctors))
        return render(request,'searchResults.html',{'doctors':doctors})
def docInfo(request,pk):
    doctor=User.objects.get(pk=pk)
    user=request.user
    if doctor in user.patientprofile.providers.all():
        bookmark_status=True
        bookmark_text='unbookmark'
    else:
        bookmark_status=False
        bookmark_text='bookmark'
    if request.method=='POST':
        print('got the request')
        if bookmark_status:
            print('recognizes bookmarked as true')
            user.patientprofile.providers.remove(doctor)
            user.save()
            bookmark_text='bookmark'
        else:
            print('recognizes bookmarked as false')
            user.patientprofile.providers.add(doctor)
            user.save()
            bookmark_text='unbookmark'
    return render(request,'docInfo.html',{'doctor':doctor,'bookmark_text':bookmark_text})

def loginView(request):
    form=loginForm
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'form':form,'error':'user not valid'})
    else:
        return render(request,'login.html',{'form':form})

def whatkindinfo(request):
    return render(request, 'whatkindinfo.html')

def qcinfo(request):
    return render(request, 'qcinfo.html')

def booking(request):
    return render(request, 'booking.html')

def triage(request):
    return render(request, 'triage.html')

