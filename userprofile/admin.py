from django.contrib import admin

# Register your models here.
from .models import Profile, Course

admin.site.register(Course)
admin.site.register(Profile)

