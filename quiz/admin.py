from django.contrib import admin
from .models import Question, QuestionList


# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionList)

