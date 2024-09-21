from django.urls import re_path
from .views import ClassOfStudentView, StudentView

urlpatterns = [
    re_path('student/register/', StudentView.as_view()),
    re_path('student/list/(?P<classId>\d+)/$', StudentView.as_view()),
    re_path('class/register/', ClassOfStudentView.as_view()),
    re_path('class/list/(?P<company>\d+)/$', ClassOfStudentView.as_view())
]