from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from .models import User
from .forms import DoctorSignupForm,PatientSignupForm

# Create your views here.

class DocSignupView(CreateView):
    model=User
    form_class=DoctorSignupForm
    template_name='signupForm.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type']='doc'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect()#something goes in the redirect here but being real idk what