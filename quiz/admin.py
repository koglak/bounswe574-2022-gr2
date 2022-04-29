from django.contrib import admin
from .models import Question, QuestionList, Score, Case, CaseResult, CaseRating


# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionList)
admin.site.register(Score)
admin.site.register(Case)
admin.site.register(CaseResult)
admin.site.register(CaseRating)


