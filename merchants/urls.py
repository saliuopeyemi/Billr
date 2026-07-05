from django.urls import path
from . import views


urlpatterns = [
    path("register/",views.MerchantRegisterView.as_view(),name="Merchant-Register"),
    path("",views.RetrieveMerchantDetailView.as_view(),name="Retrieve-Merchant"),
    path("plan/",views.PlanView.as_view(),name="Plan"),
]
