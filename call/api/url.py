from django.urls import re_path
from .views import ClassOfStudentView, StudentView, CallView, ReportCallView

urlpatterns = [
    re_path('call/register/', CallView.as_view()),
    re_path('call/report/(?P<classId>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', ReportCallView.as_view()),
    re_path('student/register/', StudentView.as_view()),
    re_path('student/list/(?P<classId>\d+)/$', StudentView.as_view()),
    re_path('class/register/', ClassOfStudentView.as_view()),
    re_path('class/list/(?P<company>\d+)/$', ClassOfStudentView.as_view())
]