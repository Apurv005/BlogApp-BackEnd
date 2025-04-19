# blog/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
import json

@csrf_exempt  # (If you haven't added authentication yet)
def create_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            title = data.get('title')
            content = data.get('content')

            # Input Validation
            if not title or not content:
                return JsonResponse(
                    {'error': 'Both title and content are required.'},
                    status=400
                )

            post = Post.objects.create(title=title, content=content)

            return JsonResponse({
                'message': 'Post created successfully',
                'post': {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'created_at': post.created_at
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Exception as e:
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
