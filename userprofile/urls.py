from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('new_course/', views.course_new, name='course_new'),

    path('<str:title>/', views.course_detail, name='course_detail'),
    path('<str:title>/edit/', views.course_edit, name='course_edit'),



]

