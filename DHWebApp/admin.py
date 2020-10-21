from django.contrib import admin
import nested_admin

from .models import Hospital,Hstaff


class HstaffAdmin(nested_admin.NestedTabularInline):
    model = Hstaff
    extra = 1

class HospitalAdmin(nested_admin.NestedModelAdmin):
    inlines = [HstaffAdmin]

admin.site.register(Hospital,HospitalAdmin)
# Register your models here.

# myModels = [models.Project, models.Client, models.About]  # iterable list
# admin.site.register(myModels)