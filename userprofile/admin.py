from django.contrib import admin

# Register your models here.
from .models import Course, Profile, Label

admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Label)