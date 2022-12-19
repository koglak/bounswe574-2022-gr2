from django.contrib import admin

# Register your models here.
from .models import Event, Profile, Course, Lecture, Comments, Question, Answer

admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Lecture)
admin.site.register(Event)
admin.site.register(Comments)
admin.site.register(Question)
admin.site.register(Answer)