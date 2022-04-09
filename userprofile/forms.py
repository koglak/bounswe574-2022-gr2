from django import forms

from .models import Profile,Course


class CourseForm(forms.ModelForm):
    class Meta:
       model = Course
       fields = ('title', 'description','img', 'collaborative_members', 'tags')
