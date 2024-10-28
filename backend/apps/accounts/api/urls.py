from django.urls import path
from .views import (
    User,
    UserView,
    UserLogin,
    UserRegister,
    RefreshTokenView,
)


from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


app_name = "user"

urlpatterns = [
    path("me/", User.as_view(), name="me"),
    path("profile/", UserView.as_view(), name="me"),
    path("login/", UserLogin.as_view(), name="login"),
    path("register/", UserRegister.as_view(), name="register"),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
]