from django.contrib import admin
from .models import Post, Answer,Label

# Model is visible by registering to admin
admin.site.register(Post)
admin.site.register(Answer)
admin.site.register(Label)
