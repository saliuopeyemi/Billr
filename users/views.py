import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsActuallyLoggedIn

from . import serializers

from utilities.tasks import send_email



class LoginView(APIView):
    permission_classes = [
        AllowAny,
    ]

    user_serializer_mapping = {
        "system_admin":serializers.SystemAdminSerializer,
        "merchant_admin":serializers.MerchantAdminSerializer,
        "customer":serializers.MerchantCustomerSerializer
    }

    def post(self,request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get("user")
            if user.is_2fa_enabled:
                serializer.save()
                return Response({"status":"OTP sent to email"},status=status.HTTP_200_OK)
            else:
                refresh_token = RefreshToken.for_user(user)
                output_serializer = self.user_serializer_mapping.get(user.user_type)
                output = {
                    "refresh":str(refresh_token),
                    "access":str(refresh_token.access_token),
                    "user":output_serializer(user,many=False).data
                }
                return Response(output,status=status.HTTP_200_OK)


class ConfirmOtpView(APIView):
    permission_classes = [
        AllowAny,
    ]

    user_serializer_mapping = {
        "system_admin":serializers.SystemAdminSerializer,
        "merchant_admin":serializers.MerchantAdminSerializer,
        "customer":serializers.MerchantCustomerSerializer
    }

    def post(self,request):
        serializer = serializers.ConfirmOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get("user")
            refresh_token = RefreshToken.for_user(user)
            output_serializer = self.user_serializer_mapping.get(user.user_type)
            output = {
                "refresh":str(refresh_token),
                "access":str(refresh_token.access_token),
                "user":output_serializer(user,many=False).data
            }
            return Response(output,status=status.HTTP_200_OK)





class TestView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self,request):
        return Response({"INSTALLED"},status=status.HTTP_200_OK)
