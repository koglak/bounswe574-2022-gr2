from django import forms

from .models import Lecture, Profile,Course, Event, Comments, Question, Answer
from django.forms import ModelForm, Select, TextInput, Form
from taggit.forms import TagWidget
from django.utils.safestring import mark_safe
from django.forms.widgets import NumberInput
from tinymce.widgets import TinyMCE

class TinyMCEWidget (TinyMCE) :
    def use_required_attribute(self, *args):
        return False
  
class CourseForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    
    class Meta:
       model = Course
       fields = ('title', 'description','img', 'collaborative_members', 'tags')
       widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name',
                }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name',
                }),
            'tags': TagWidget(),
            'img': forms.FileInput(),
                }

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Profile
        fields = ('bio', 'img')

class LectureForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Lecture
        fields = ('title', 'content')


class EventForm(forms.ModelForm):

    description = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    
    class Meta:
        model = Event
        fields = ('title', 'description', 'img', 'event_date', 'event_time', 'category', 'link', 'quota', 'duration')

        widgets = {
            'event_date': NumberInput(attrs={'type':'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'img': forms.FileInput(),
        }

class CategorySortingForm(ModelForm):
    class Meta:
        model = Event
        fields = ['category']

        widgets = {
           # Here you define what input type should the field have
           'category': Select(attrs = { 
               'required': False,
               'class': 'dropdown',
               'onchange': 'this.form.submit();',
                'name':'category'
           })
        }


class DateFilterForm(forms.Form):
    DATE_CHOICES =(
            ("Ascending", "Ascending"),
            ("Descending", "Descending"),
            )
    
    event_date = forms.CharField(
        required=False,
        widget=forms.Select(choices=DATE_CHOICES, attrs={
                'class': 'dropdown',
                'onchange': 'this.form.submit();',
                'name':'event_date'
                })
)


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('body',)
        labels = {
        'body': (''),
         }
 

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'question', 'tags')
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Title',
                }),
            'question': TinyMCEWidget(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Text',
                }),
            'tags': TagWidget(),}

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('answer',)
        labels = {
        'answer': (''),
         }
    