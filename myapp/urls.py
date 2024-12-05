from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create', views.create_post, name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]
