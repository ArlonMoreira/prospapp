from django.urls import re_path
from .views import VersionView

urlpatterns = [
    re_path('version/', VersionView.as_view()),
]