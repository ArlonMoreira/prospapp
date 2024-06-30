from django.urls import re_path
from .views import LoginView, RefreshTokenView

urlpatterns = [
    re_path('signin/', LoginView.as_view()),
    re_path('token/refresh/', RefreshTokenView.as_view())
]