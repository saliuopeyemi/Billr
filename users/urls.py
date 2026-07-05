from django.urls import path
from . import views



urlpatterns = [
    path("signin/",views.LoginView.as_view(),name="Login-View"),
    path("signin/confirm-otp/",views.ConfirmOtpView.as_view(),name="Confirm-Otp"),
]
