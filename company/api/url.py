from django.urls import re_path
from .views import PendingViews, UsersPendingViews

urlpatterns = [
    re_path('pending/', PendingViews.as_view()),
    re_path('listusers/(?P<companyId>\d+)/$', UsersPendingViews.as_view())
]