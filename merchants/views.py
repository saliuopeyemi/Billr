from os import stat
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers,models
from users.permissions import IsActuallyLoggedIn,IsAnAdmin, IsMerchantAdmin

from utilities.helpers import retrieve_query_parameter, retrieve_object


def no_objects_fails(name=""):
    raise Http404(f"Invalid {name} instance ID")

def no_parameter_fails(name=""):
    raise Http404(f"A {name} query parameter is required for this request.")

def ignore():
    pass




class MerchantRegisterView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self,request):
        serializer = serializers.MerchantRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            merchant = serializer.save()
            output = serializers.RetrieveMerchantSerializer(merchant,many=False).data
            return Response(output,status=status.HTTP_200_OK)


class RetrieveMerchantDetailView(APIView):
    permission_classes = [
        IsActuallyLoggedIn,
        IsAnAdmin
    ]

    def get(self,request):
        user = request.user
        if user.user_type == "system_admin":
            merchant_id = retrieve_query_parameter(request,"merchant_id",ignore)
            if not merchant_id:
                all_merchants = models.Merchant.objects.all()
                output = serializers.MiniMerchantSerializer(all_merchants,many=True).data
            else:
                merchant = retrieve_object(merchant_id,models.Merchant,no_objects_fails,"Merchant")
                output = serializers.RetrieveMerchantSerializer(merchant,many=False).data
        else:
            merchant = user.related_merchant
            output = serializers.MaxMerchantSerializer(merchant,many=False).data
        return Response(output,status=status.HTTP_200_OK)


class PlanView(APIView):
    permission_classes = [
        IsActuallyLoggedIn,
        IsMerchantAdmin,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.CreatePlanSerializer(data=request.data,context={"user":user})
        if serializer.is_valid(raise_exception=True):
            plan = serializer.save()
            output = serializers.RetrievePlanSerializer(plan,many=False).data
            return Response(output,status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        plan_id = retrieve_query_parameter(request,"plan_id",ignore)
        if not plan_id:
            all_plans = models.Plan.objects.filter(merchant=user.related_merchant).order_by("id")
            output = serializers.RetrievePlanSerializer(all_plans,many=True).data
        else:
            plan = retrieve_object(plan_id,models.Plan,no_objects_fails,"Plan")
            output = serializers.RetrievePlanSerializer(plan,many=False).data
        return Response(output,status=status.HTTP_200_OK)






class TestView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self,request):
        return Response({"INSTALLED"},status=status.HTTP_200_OK)
