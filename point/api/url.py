from django.urls import re_path
from .views import LocalViews

urlpatterns = [
    re_path('register/', LocalViews.as_view())
]