from django.contrib.auth import login,authenticate
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from .models import User,DoctorProfile
from .forms import DoctorSignupForm,PatientSignupForm,SearchCrieteriaForm,loginForm
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.views.generic.edit import FormView
from django.views import View
from .models import Language
from django import forms

# Create your views here.
#these views might be ass go back over them later


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
    print('print does work so like wtf')
    return render(request,'home.html')

def triage(request):
    return render(request,'triage.html')

class searchCriteria(FormView):
    template_name='searchCriteria.html'
    form_class=SearchCrieteriaForm

    def form_valid(self,form):
        print('got here??')
        #distance=form.cleaned_data.get('distance')
        specialty=form.cleaned_data.get('specialty')
        female=form.cleaned_data.get('female')
        male=form.cleaned_data.get('male')
        #print(distance)
        print(specialty)
        print(female)
        print(male)
        return redirect('searchresults',specialty,female,male)

#i removed an if request.method==post from this, should maybe check if that needs to be added back
class searchResults(View):
    def get(self,request,distance,specialty,female,male):
        me=request.user
        here=me.location
        languages=me.languages.all()
        accessibility=me.acessibility
        doctors=[]
        query=Q(is_doctor=True)&Q(location__distance_lt=(here,Distance(km=distance)))&Q(profile__specialty=specialty)
        print(me.location)
        if accessibility==True:
            query&=Q(accessibility=True)
        if male==True:
            query&=Q(is_male=True)
        if female==True:
            query&=Q(is_female=True)
            query&=Q(is_female=True)
        for language in languages:
            doctors+=language.user_set.filter(query)
        print(len(doctors))
        #is this ass? maybe
        doctors=list(set(doctors))
        return render(request,'searchResults.html',{'doctors':doctors})
def docInfo(request,pk):
    doctor=User.objects.get(pk=pk)
    user=request.user
    #this code might be shit go back over later
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
            user.patientprofile__providers.remove(doctor)
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


