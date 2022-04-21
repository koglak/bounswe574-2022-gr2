from django.forms import ModelForm
from .models import *
from django import forms

 
 
class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields="__all__"

class QuizForm(ModelForm):

    #question_quantity = forms.IntegerField(widget=forms.NumberInput, max_value=10)

    class Meta:
        model=QuestionList
        fields=('title', )


class CaseForm(ModelForm):

    class Meta:
        model=Case
        fields=('title','description')