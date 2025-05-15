from django.contrib import admin
from .models import Language,DoctorProfile,User,PatientProfile
#from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Image

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
class ImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 200px; max-height: 200px"/>'. format(obj.image.url))
# Register your models here.



