from django.urls import path

from . import views
from .views import create_post, get_all_posts

urlpatterns = [
    path('create/', create_post, name='create-post'),
path('delete/<int:post_id>/', views.delete_post, name='delete-post'),
path('api/posts/', get_all_posts, name='get-all-posts'),

]