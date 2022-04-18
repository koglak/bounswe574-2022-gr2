from django.urls import path
from . import views

urlpatterns = [
    path('<str:title>/quiz/', views.quiz_detail,name='quiz_detail'),
    path('addQuestion/', views.question_add,name='addQuestion'),
    #path('<str:title>', views.quiz_detail,name='quiz_detail'),


]