from django.utils import timezone

from rest_framework import serializers


from merchants.serializers import RetrieveMerchantSerializer

from . import models


from utilities.tasks import send_email

import random
import string




EMAIL_OTP_BODY = '''
        Hello,

        Your One-Time-Password for login is provided below.

        {OTP}

        This code is valid for only 5 minutes.
    '''




class SystemAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ["id","full_name","email","user_type"]

class MerchantAdminSerializer(serializers.ModelSerializer):
    related_merchant = RetrieveMerchantSerializer()

    class Meta:
        model = models.User
        fields = ["id","full_name","email","user_type","related_merchant"]

class MerchantCustomerSerializer(serializers.ModelSerializer):
    related_merchant = RetrieveMerchantSerializer()

    class Meta:
        model = models.User
        fields = ["id","full_name","email","user_type","related_merchant"]





class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    def validate(self,data):
        email = data.get("email")
        password = data.get("password")
        user = models.User.objects.filter(email=email)
        if not user.exists():
            raise serializers.ValidationError("Invalid Email/Password")

        user = user.first()
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid Email/Password")
        data["user"] = user
        return data

    def create(self,validated_data):
        user = validated_data.get("user")
        email = user.email
        otp = "".join(random.choices(string.digits,k=6))

        format = {
            "OTP": otp
        }
        body = EMAIL_OTP_BODY.format(**format)
        send_email.delay(subject="Login OTP",body=body,recipients=[email])

        models.LoginOtp.objects.create(email=email,otp=otp)
        return {}


class ConfirmOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=50)

    def validate(self,data):
        email = data.get("email")
        otp = data.get("otp")
        login_instance = models.LoginOtp.objects.filter(email=email,otp=otp)
        if not login_instance.exists():
            raise serializers.ValidationError("Invalid OTP")
        now = timezone.now()
        diff = (now-login_instance.first().timestamp).total_seconds()//60
        if diff > 5:
            login_instance.delete()
            raise serializers.ValidationError("Expired OTP")

        login_instance.delete()
        user = models.User.objects.filter(email=email).first()
        data["user"] = user
        return data
