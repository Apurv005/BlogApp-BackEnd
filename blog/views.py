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


@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'DELETE':
        try:
            post = Post.objects.get(id=post_id)
            deleted_data = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
            }
            post.delete()
            return JsonResponse({
                'message': 'Post deleted successfully!',
                'deleted_post': deleted_data
            }, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post with the provided ID does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_all_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        post_list = []

        for post in posts:
            post_list.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at
            })

        return JsonResponse({'posts': post_list}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
