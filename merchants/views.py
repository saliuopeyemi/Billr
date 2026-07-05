from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from users.permissions import IsActuallyLoggedIn




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


            







class TestView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self,request):
        return Response({"INSTALLED"},status=status.HTTP_200_OK)
