from django.contrib import admin
from .models import Language,DoctorProfile,User,PatientProfile
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets+ (
        (                      
            'additionalfields', # you can also use None 
            {
                'fields': (
                    'is_doctor',
                    'is_patient',
                    'name',
                    'acessibility',
                    'location',
                    'address',
                    'languages',
                ),
            },
        ),
    )


#admin.site.register(User,UserAdmin)
admin.site.register(Language)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)

class UserAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')


