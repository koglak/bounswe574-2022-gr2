from django.urls import path
from . import views

urlpatterns = [
    path('<str:title>/quiz/', views.quiz_detail,name='quiz_detail'),
    path('<str:title>/quiz_add/', views.question_add,name='question_add'),
    #path('<str:title>', views.quiz_detail,name='quiz_detail'),
    path('<str:title>/quiz_create/', views.quiz_create,name='quiz_create'),
    path('<str:title>/quiz_delete',views.quiz_delete,name='quiz_delete'),
    path('<str:title>/case_create/', views.case_create,name='case_create'),
    path('<str:title>/case_edit/', views.case_edit,name='case_edit'),
    path('<str:title>/case_delete/', views.case_delete,name='case_delete'),
    path('<str:title>/case_detail/', views.case_detail,name='case_detail'),
    path('<str:title>/submit_assignment/', views.submit_assignment, name='submit_assignment'),
    #path('<str:title>/delete_submission/', views.delete_submission, name = 'delete_submission'),

    path('<str:title>/case_grade/', views.case_grade,name='case_grade'),
    path('<int:pk>/case_rate',views.case_rate,name='case_rate'),
    path('case/search_result',views.search_case,name='search_case'),



]