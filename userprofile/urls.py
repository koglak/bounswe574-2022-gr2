from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('new_course/', views.course_new, name='course_new'),
    path('<str:title>/', views.course_detail, name='course_detail'),
    path('<str:title>/edit/', views.course_edit, name='course_edit'),
    path('tag/<str:tag>', views.course_tag_detail, name='course_tag_detail'),
    path('<str:title>/delete-post',views.delete_course,name='delete_course'),
    path('profile/<str:name>', views.other_user_profile, name='other_user_profile'),
    path('<str:title>/rate',views.course_rate,name='course_rate'),

]

