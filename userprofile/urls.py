from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('learn/',views.learn_page,name='learn'),
    path('new_course/', views.course_new, name='course_new'),
    path('<str:title>/', views.course_detail, name='course_detail'),
    path('<str:title>/course_edit/', views.course_edit, name='course_edit'),
    path('tag/<str:tag>', views.course_tag_detail, name='course_tag_detail'),
    path('<str:title>/course_delete',views.delete_course,name='delete_course'),
    path('profile/<str:name>', views.other_user_profile, name='other_user_profile'),
    path('<str:title>/rate',views.course_rate,name='course_rate'),
    path('lecture/<int:pk>',views.lecture_detail,name='lecture_detail'),
    path('edit/<int:pk>', views.profile_edit, name='profile_edit'),
    path('course/search_result',views.search_course,name='search_course'),
    path('<int:pk>/enroll',views.course_enroll,name='course_enroll'),
    path('<int:pk>/drop',views.course_drop,name='course_drop'),
    path('lecture_new/<int:pk>', views.lecture_new, name='lecture_new'),
    path('<int:pk>/lecture_edit/', views.lecture_edit, name='lecture_edit'),
    path('<str:title>/lecture_delete',views.delete_lecture,name='delete_lecture'),
    path('<str:title>/upcoming_events',views.event_list,name='event_list'),
    path('<str:title>/past_events',views.past_event,name='past_event'),
    path('<str:title>/quiz_page',views.quiz_page,name='quiz_page'),
    path('<str:title>/case_page',views.case_page,name='case_page'),
    path('<str:title>/event_new/', views.event_new,name='event_new'),
    path('event_edit/<int:pk>', views.event_edit,name='event_edit'),
    path('event_enroll/<int:pk>', views.event_enroll,name='event_enroll'),
]

