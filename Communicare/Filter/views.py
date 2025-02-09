from django.contrib.auth import login
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from .models import User,DoctorProfile
from .forms import DoctorSignupForm,PatientSignupForm,SearchCrieteriaForm
#from django.contrib.gis.measure import Distance
#from django.contrib.gis.geos import Point
from django.db.models import Q
from django.views.generic.edit import FormView
from django.views import View
# Create your views here.
#these views might be ass go back over them later

#idk if i should maybe be storing this somewhere else

class DocSignupView(CreateView):
    model=User
    form_class=DoctorSignupForm
    template_name='signupForm.html'

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
    def get(self,request,specialty,female,male):
        me=request.user
        #here=me.location
        languages=me.languages.all()
        accessibility=me.acessibility
        doctors=[]
        query=Q(is_doctor=True)&Q(profile__specialty=specialty)#&Q(location__distance_lt=(here,Distance(km=distance)))
        print(me.location)
        if accessibility==True:
            query&=Q(accessibility=True)
        if male==True:
            query&=Q(is_male=True)
        if female==True:
            query&=Q(is_female=True)
        for language in languages:
            doctors+=language.user_set.filter(query)
        print(len(doctors))
        return render(request,'searchResults.html',{'doctors':doctors})
def docInfo(request,pk):
    doctor=User.objects.get(pk=pk)
    name=doctor.name
    langs=[language.lang for language in doctor.languages.all()]
    return render(request,'docInfo.html',{'doctor':doctor})