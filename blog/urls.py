from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name="post_detail"),
    path('post/add/', views.post_add, name="post_add"),
    path('post/edit/<int:pk>/', views.post_edit, name="post_edit"),
    path('post/draft/', views.post_draft, name="post_draft"),
    path('post/publish/<int:pk>', views.post_publish, name="post_publish"),
    path('post/delete/<int:pk>/', views.post_delete, name="post_delete"),
    path('post/<int:pk>/comment/', views.post_add_comment, name="post_add_comment"),
]
