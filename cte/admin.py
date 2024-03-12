from django.contrib import admin
from .models import School, Student, Business, Job, HoursRequest

# Register your models here.
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Business)
admin.site.register(Job)
admin.site.register(HoursRequest)