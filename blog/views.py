from django.shortcuts import render

# Create your views here.
# blog/views.py

from django.http import JsonResponse
from .models import Post
import json

def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        title = data.get('title')
        content = data.get('content')

        post = Post.objects.create(title=title, content=content)

        return JsonResponse({
            'message': 'Post created successfully',
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content
            }
        }, status=201)
