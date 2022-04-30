from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity,name='activity'),
    path('activity_new/', views.activity_new,name='activity_new'),
    path('activity_edit/<int:pk>', views.activity_edit,name='activity_edit'),
    path('activity_enroll/<int:pk>', views.activity_enroll,name='activity_enroll'),



]