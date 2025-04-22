from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
def register(request):
    """User registration"""
    data = request.data
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
    return Response({'message': 'User registered successfully'}, status=201)


@api_view(['POST'])
def login(request):
    """User login and JWT token generation"""
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        print(username, password)
        # Authenticate the user
        user = User.objects.get(username=username)
        if user.check_password(password):
            # If credentials are correct, generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'access': access_token,
                'refresh': str(refresh),
                'username': user.username,
                'id': user.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def logout(request):
    """Logout by blacklisting the refresh token"""
    try:
        token = request.data.get('refresh_token')
        if token:
            RefreshToken(token).blacklist()
        return Response({'message': 'Logged out successfully'}, status=200)
    except Exception:
        return Response({'error': 'Invalid token'}, status=400)

class VerifyTokenView(APIView):
    print("hello 60")
    permission_classes = [IsAuthenticated]
    print("hello 61")

    def get(self, request):
        # If the request is authenticated, return a success message
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)