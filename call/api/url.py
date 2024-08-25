from django.urls import re_path
from .views import ClassOfStudentView

urlpatterns = [
    re_path('register/', ClassOfStudentView.as_view()),
    re_path('list/(?P<company>\d+)/$', ClassOfStudentView.as_view())
]