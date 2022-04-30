
from django import forms

from .models import Activity
import datetime
from django.forms.widgets import DateInput
from django.forms.widgets import NumberInput


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = ('title', 'description', 'start_time')

        widgets = {
            'start_time': NumberInput(attrs={'type':'date'}),
        }
