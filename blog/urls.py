from django.urls import path

from . import views
from .views import create_post

urlpatterns = [
    path('create/', create_post, name='create-post'),
path('delete/<int:post_id>/', views.delete_post, name='delete-post'),

]