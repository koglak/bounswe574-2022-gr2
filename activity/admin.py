from django.contrib import admin
from .models import Activity

# Model is visible by registering to admin
admin.site.register(Activity)