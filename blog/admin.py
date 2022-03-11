from django.contrib import admin
from .models import Post

# Model is visible by registering to admin
admin.site.register(Post)
