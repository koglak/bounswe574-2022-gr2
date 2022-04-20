from django.urls import path
from . import views

urlpatterns = [
    path('<str:title>/quiz/', views.quiz_detail,name='quiz_detail'),
    path('<str:title>/quiz_add/', views.question_add,name='question_add'),
    #path('<str:title>', views.quiz_detail,name='quiz_detail'),
    path('<str:title>/quiz_create/', views.quiz_create,name='quiz_create'),
]