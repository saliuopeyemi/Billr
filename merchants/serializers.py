from django.db.models import Q
from django.db import transaction

from rest_framework import serializers

from . import models
from users.models import User

from .utils import generate_test_api_key
import uuid



class MerchantRegisterSerializer(serializers.Serializer):
    business_name = serializers.CharField(max_length=250)
    business_email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=50)
    business_type = serializers.ChoiceField(choices=models.BUSINESS_TYPE)
    web_url = serializers.CharField(required=False)
    full_name = serializers.CharField(max_length=250)
    password1 = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)

    def validate_business_email(self,email):
        if models.Merchant.objects.filter(business_email=email).exists() or User.objects.filter(email=email).exists():
            raise serializers.ValidationError("An account with this email is already in existence.")
        return email

    def validate(self,data):
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 != password2:
            raise serializers.ValidationError("Password Mismatch.")
        if len(password1) < 6:
            raise serializers.ValidationError("Password too short.")

        return data

    def create(self,validated_data):
        email = validated_data.get("business_email")
        full_name = validated_data.get("full_name")
        password = validated_data.get("password1")

        merchant_payload = {
            "business_name":validated_data.get("business_name"),
            "business_email":email,
            "phone_number":validated_data.get("phone_number"),
            "business_type":validated_data.get("business_type"),
            "web_url":validated_data.get("web_url")
        }
        with transaction.atomic():
            merchant = models.Merchant.objects.create(**merchant_payload)
            User.objects.create_user(username=str(uuid.uuid4()),email=email,full_name=full_name,password=password,related_merchant=merchant,user_type="merchant_admin")

            apikey_payload = {
                "merchant_id":merchant.id,
                "merchant_name":merchant.business_name,
                "merchant_email":merchant.business_email
            }
            test_apikey = generate_test_api_key(apikey_payload,key_type="TEST")
            prod_apikey = generate_test_api_key(apikey_payload,key_type="PROD")
            merchant.test_api_key = test_apikey
            merchant.live_api_key = prod_apikey
            merchant.save()

        return merchant


class RetrieveMerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Merchant
        fields = ["id","business_name","business_email","phone_number","business_type","web_url","test_api_key"]

class MiniMerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Merchant
        fields = ["id","business_email","business_name","phone_number"]

class MaxMerchantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Merchant
        fields = "__all__"

class CreatePlanSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=40,decimal_places=2)
    billing_interval = serializers.ChoiceField(choices=models.BILLING_INTERVAL)
    billing_interval_in_days = serializers.IntegerField(required=False)
    trial_period_in_days = serializers.IntegerField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.caller = self.context["user"]

    def validate_name(self,name):
        if models.Plan.objects.filter(name__iexact=name,merchant=self.caller.related_merchant).exists():
            raise serializers.ValidationError("A Plan with this name already exists.")
        return name

    def validate(self,data):
        billing_interval = data.get("billing_interval")
        if billing_interval == "custom":
            billing_interval_in_days = data.get("billing_interval_in_days")
            if not billing_interval_in_days:
                raise serializers.ValidationError("billing_intrval_in_days must be provided for custom billing")
        else:
            #Ensure billing_interval_in_days property is always Null when not custom
            data.pop("billing_interval_in_days",None)

        return data

    def create(self,validated_data):
        validated_data["merchant"] = self.caller.related_merchant
        plan = models.Plan.objects.create(**validated_data)
        return plan


class RetrievePlanSerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()

    class Meta:
        model = models.Plan
        fields = ["id","name","description","price","billing_interval","billing_interval_in_days","trial_period_in_days","subscribers","status","created"]

    def get_subscribers(self,obj):
        return 0

class UpdatePlanSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=40,decimal_places=2)
    billing_interval = serializers.ChoiceField(choices=models.BILLING_INTERVAL)
    billing_interval_in_days = serializers.IntegerField(required=False)
    trial_period_in_days = serializers.IntegerField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.caller = self.context["user"]

    def validate_name(self,name):
        if models.Plan.objects.filter(name=name,merchant=self.caller.related_merchant).exclude(name=name).exists():
            raise serializers.ValidationError("A Plan with this name already exists.")
        return name

    def validate(self,data):
        billing_interval = data.get("billing_interval")
        if billing_interval:
            if billing_interval == "custom":
                billing_interval_in_days = data.get("billing_interval_in_days")
                if not billing_interval_in_days:
                    raise serializers.ValidationError("billing_intrval_in_days must be provided for custom billing")
            else:
                #Ensure billing_interval_in_days property is always Null when not custom
                data.pop("billing_interval_in_days",None)

            return data
        return data

    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance

