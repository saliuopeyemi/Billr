from django.urls import path
from . import views


urlpatterns = [
    path("register/",views.MerchantRegisterView.as_view(),name="Merchant-Register"),
]
