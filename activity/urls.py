from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity,name='activity'),
    path('activity_new/', views.activity_new,name='activity_new'),


]