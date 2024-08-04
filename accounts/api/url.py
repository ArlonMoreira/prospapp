from django.urls import re_path
from .views import LoginView, RefreshTokenView, RegisterView, MeView, LogoutView

urlpatterns = [
    re_path('signin/', LoginView.as_view()),
    re_path('logout/', LogoutView.as_view()),
    re_path('register/', RegisterView.as_view()),
    re_path('token/refresh/', RefreshTokenView.as_view()),
    re_path('me/', MeView.as_view())
]