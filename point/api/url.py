from django.urls import re_path
from .views import LocalViews, GetLocalViews

urlpatterns = [
    re_path('register/', LocalViews.as_view()),
    re_path('list/(?P<companyId>\d+)/$', GetLocalViews.as_view())
]