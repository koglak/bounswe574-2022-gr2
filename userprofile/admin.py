from django.contrib import admin

# Register your models here.
from .models import Event, Profile, Course, Lecture

admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Lecture)
admin.site.register(Event)

