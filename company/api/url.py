from django.urls import re_path
from .views import PendingViews

urlpatterns = [
    re_path('pending/', PendingViews.as_view()),
]