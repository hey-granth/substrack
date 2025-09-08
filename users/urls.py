from django.urls import path
from .views import register_view, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),    # log in
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
