from django.urls import path
from . import views


urlpatterns = [
    path("plans/",views.RetrieveMerchantPlanView.as_view(),name="Retrieve-Merchant-Plan"),
    #path("customer/subscribe/",views.CustomerSubscribeView.as_view(),name="Customer-Subscribe"),
]
