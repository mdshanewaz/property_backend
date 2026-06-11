from django.urls import path
from user_app.views import register_user_view, profile_user_view, Custom_TokenObtainPairView, Custom_TokenRefreshView, logoutView, is_authenticated_view, otp_validation_view, email_otp_reset_pass_view, reset_pass_view, profile_edit_view
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

# Create your urls here.
# app_name = 'user_app'

urlpatterns = [
    path("register/", register_user_view, name="register"),
    path("otp/", otp_validation_view, name="otp"),
    path("mail/", email_otp_reset_pass_view, name="mail"),
    path('reset/', reset_pass_view, name="reset"),
    path("profile/", profile_user_view, name="profile"),
    path('update/', profile_edit_view, name="update"),

    path("token/", Custom_TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", Custom_TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", logoutView, name="logout"),
    path("authenticated/", is_authenticated_view, name="authenticated")
]