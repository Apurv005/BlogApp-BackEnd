from django.urls import path
from .views import register, login, logout, VerifyTokenView
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
path("verify-token/", VerifyTokenView.as_view(), name="verify-token"),

]