from django.urls import re_path
from .views import ReportPointView, LocalDisableView, LocalViews, GetLocalViews, RegisterPointView, RegisterPointActualView, RemovePointTodayView, LocalUpdateView

urlpatterns = [
    re_path('local/register/', LocalViews.as_view()),
    re_path('local/list/(?P<companyId>\d+)/$', GetLocalViews.as_view()),
    re_path('local/disabled/(?P<localId>\d+)/$', LocalDisableView.as_view()),
    re_path('local/change/(?P<localId>\d+)/$', LocalUpdateView.as_view()),
    re_path('register/', RegisterPointView.as_view()),
    re_path('current/(?P<localId>\d+)/$', RegisterPointActualView.as_view()),
    re_path('remove/today/(?P<pointId>\d+)/$', RemovePointTodayView.as_view()),
    re_path('report/', ReportPointView.as_view()),
]