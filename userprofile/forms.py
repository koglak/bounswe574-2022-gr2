from django import forms

from .models import Profile, Course, Label


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description','img')

class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields =('name',)       