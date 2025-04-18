from django.urls import re_path
from .views import EditView, LoginView, RefreshTokenView, RegisterView, MeView, LogoutView, ResetPasswordView, RegisterVerificationView, CheckVerificationView, GenerateCodeAgainView

urlpatterns = [
    re_path('signin/', LoginView.as_view()),
    re_path('logout/', LogoutView.as_view()),
    re_path('register/', RegisterView.as_view()),
    re_path('register_v2/', RegisterVerificationView.as_view()),
    re_path('register_check/', CheckVerificationView.as_view()),
    re_path('register_refresh_code/', GenerateCodeAgainView.as_view()),
    re_path('token/refresh/', RefreshTokenView.as_view()),
    re_path('me/', MeView.as_view()),
    re_path('change/', EditView.as_view()),
    re_path('resetpassword/', ResetPasswordView.as_view())
]