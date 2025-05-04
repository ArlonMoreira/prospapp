from django.urls import re_path
from .views import LocalViews, GetLocalViews, RegisterPointView, RegisterPointActualView

urlpatterns = [
    re_path('local/register/', LocalViews.as_view()),
    re_path('local/list/(?P<companyId>\d+)/$', GetLocalViews.as_view()),
    re_path('register/', RegisterPointView.as_view()),
    re_path('current/(?P<localId>\d+)/$', RegisterPointActualView.as_view()),
]