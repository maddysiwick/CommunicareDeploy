"""
URL configuration for Communicare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Filter import views
from django.contrib.auth import views as authViews
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('signup/',views.triage,name='signup'),
    path('signup/doctor/',views.DocSignupView.as_view(),name='docSignup'),
    path('signup/patient/',views.PatientSignupView.as_view(),name='patientSignup'),
    path('/',views.home,name='home'),
    path('search/',views.searchCriteria.as_view(),name='searchcriteria'),
    path('search/results/<distance>/<specialty>/<female>/<male>/',views.searchResults.as_view(),name='searchresults'),
    path('search/results/<int:pk>/',views.docInfo,name='docinfo'),
    path('whatkindinfo/',views.whatkindinfo,name='whatkindinfo'),
    path('qcinfo/',views.qcinfo,name='qcinfo'),
    path('booking/',views.booking,name='booking'),
    path('logout/',authViews.LogoutView.as_view(),name='logout'),
    path('login',views.loginView,name='login'),
    path('triage', views.triage, name='triage'),
    path('language-autocomplete/',views.languageAutocomplete.as_view(),name='language-autocomplete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)