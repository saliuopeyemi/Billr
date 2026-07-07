from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from . import serializers,models
from merchants.models import Merchant
from merchants.serializers import RetrievePlanSerializer

from merchants.middleware import MerchantIntegration

from utilities.helpers import ensure_merchant_apikey_is_active,retrieve_object,retrieve_query_parameter

import uuid
import requests


def inactive_merchant_apikey_fails():
    raise Http404("Merchant's APIKey is Inactive")

def no_merchant_fails():
    raise Http404("Merchant Not found.")



class RetrieveMerchantPlanView(APIView):
    authentication_classes = [
        MerchantIntegration,
    ]

    permission_classes = [
        AllowAny,
    ]

    def get(self,request):
        payload = request.auth 
        merchant_id = payload.get("merchant_id")
        merchant = Merchant.objects.filter(id=merchant_id).first()
        if not merchant:
            return Response({"error":"Merchant Not found"},status=status.HTTP_400_BAD_REQUEST)
        ensure_merchant_apikey_is_active(request,merchant,inactive_merchant_apikey_fails)
        plans = merchant.plan_set.all()
        output = RetrievePlanSerializer(plans,many=True).data
        return Response(output,status=status.HTTP_200_OK)


class CustomerSubscribeView(APIView):
    authentication_classes = [
        MerchantIntegration,
    ]
    permission_classes = [
        AllowAny,
    ]

    def post(self,request):
        payload = request.auth
        merchant_id = payload.get("merchant_id")
        merchant = retrieve_object(merchant_id,Merchant,no_merchant_fails)
        ensure_merchant_apikey_is_active(request,merchant,inactive_merchant_apikey_fails)
        serializer = serializers.CustomerSubscribeSerializer(data=request.data,context={"merchant":merchant})
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            plan = data.get("plan")
            amount = data.get("amount")
            customer = serializer.save()

            

