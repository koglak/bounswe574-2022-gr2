from django import forms

from .models import Lecture, Profile,Course, Event
from django.forms import ImageField, ModelForm, Select, TextInput
from taggit.forms import TagWidget
from django.utils.safestring import mark_safe
from django.forms.widgets import NumberInput



CATEGORY_CHOICES =(
    ("All", "All"),
    ("Outside", "Outside"),
    ("Workshop", "Workshop"),
    ("Social", "Social"),
    ("Presentation", "Presentation"),
    ("Introductory", "Introductory"),
    ("Training", "Training"),
    )
  
class CourseForm(forms.ModelForm):
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
    class Meta:
        model = Profile
        fields = ('bio', 'img')

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('title', 'content')


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'description', 'img', 'event_date', 'event_time', 'category', 'link', 'quota')

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
               'class': 'form-control',
               'onchange': 'this.form.submit();',
               "name":"category"
           })
        }