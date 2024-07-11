from django.urls import re_path
from .views import StatusViews

urlpatterns = [
    re_path('status/', StatusViews.as_view()),
]