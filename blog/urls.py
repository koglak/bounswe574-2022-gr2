from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/new/', views.question_new, name='question_new'),
    path('question/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('question/', views.question, name='question'),
    path('like/<int:pk>', views.LikeView, name='like_post'),
    path('like/question', views.LikeViewList, name='like_post_list'),
    path('dislike/<int:pk>', views.DislikeView, name='dislike_post'),
    path('dislike/question', views.DislikeViewList, name='dislike_post_list'),
    path('label/<str:tag>', views.question_tag_detail, name='question_tag_detail'),
    path('<int:pk>/delete-question',views.delete_question,name='delete_question'),



]