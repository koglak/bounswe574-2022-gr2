from django.urls import path
from . import views

urlpatterns = [
    path('<str:title>/quiz/', views.quiz_detail,name='quiz_detail'),
    path('<str:title>/quiz_add/', views.question_add,name='question_add'),
    #path('<str:title>', views.quiz_detail,name='quiz_detail'),
    path('<str:title>/quiz_create/', views.quiz_create,name='quiz_create'),
    path('<str:title>/quiz_delete',views.quiz_delete,name='quiz_delete'),
    path('<str:title>/case_create/', views.case_create,name='case_create'),
    path('<str:title>/case_detail/', views.case_detail,name='case_detail'),
    path('comment/', views.comment_new, name='comment'),
    path('<int:pk>/delete-comment',views.delete_comment,name='delete_comment'),
    path('like/<int:pk>', views.LikeView_comment, name='like_comment'),
    path('like/comment', views.LikeViewList_comment, name='like_comment_list'),
    path('dislike/<int:pk>', views.DislikeView_comment, name='dislike_comment'),
    path('dislike/question', views.DislikeViewList_comment, name='dislike_comment_list'),
    path('<int:pk>/delete-question',views.delete_comment,name='delete_comment'),
    path('like-answer/<int:pk>', views.ReplyCommentLikeView, name='like_replycomment'),
    path('dislike-answer/<int:pk>', views.ReplyCommentDislikeView, name='dislike_replycomment'),

    path('<str:title>/case_grade/', views.case_grade,name='case_grade'),
    path('<int:pk>/case_rate',views.case_rate,name='case_rate'),



]