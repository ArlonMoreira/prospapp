from django.urls import re_path
from .views import RelateClassAndStudent, ClassOfStudentRelateView, StudentDisableView, StudentUpdateView, ClassOfStudentDisableView, ClassOfStudentUpdateView, ClassOfStudentView, StudentView, CallView, ReportCallView

urlpatterns = [
    re_path('call/register/', CallView.as_view()),
    re_path('call/report/(?P<classId>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', ReportCallView.as_view()),
    re_path('student/register/', StudentView.as_view()),
    re_path(r'^student/list/(?P<classId>\d+)(?:/(?P<date>\d+))?/$', StudentView.as_view()),
    re_path('student/change/(?P<student>\d+)/$', StudentUpdateView.as_view()),
    re_path('student/disabled/(?P<student>\d+)/$', StudentDisableView.as_view()),
    re_path('class/register/', ClassOfStudentView.as_view()),
    re_path('class/list/(?P<company>\d+)/$', ClassOfStudentView.as_view()),
    re_path('class/relate/register/', ClassOfStudentRelateView.as_view()),
    re_path('class/relate/list/(?P<company>\d+)/$', ClassOfStudentRelateView.as_view()),     
    re_path('class/relate/users/(?P<company>\d+)/(?P<classId>\d+)/$', RelateClassAndStudent.as_view()),   
    re_path('class/relate/addusers/$', RelateClassAndStudent.as_view()),  
    re_path('class/change/(?P<Class>\d+)/$', ClassOfStudentUpdateView.as_view()),
    re_path('class/disabled/(?P<Class>\d+)/$', ClassOfStudentDisableView.as_view())
]