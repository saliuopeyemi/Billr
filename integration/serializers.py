import email
from rest_framework import serializers

from users.models import User

from merchants.models import Plan

import uuid
import random
import string
import json



class CustomerSubscribeSerializer(serializers.Serializer):
    customer_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=40,decimal_places=2)
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    def validate_plan(self,plan):
        merchant = self.context["merchant"]
        if plan.merchant != merchant:
            raise serializers.ValidationError("This Plan is not owned by your merchant")
        return plan

    def create(self,validated_data):
        customer_email = validated_data.get("customer_email")
        amount = validated_data.get("amount")
        plan = validated_data.get("plan")
        customer = User.objects.filter(email=customer_email).first()
        if not customer:
            password = random.choices(string.digits+string.ascii_lowercase+string.ascii_uppercase,k=10)
            password = "".join(password)
            print(password)
            username = str(uuid.uuid4())
            customer = User.objects.create_user(email=customer_email,username=username,password=password,user_type="customer")
            
        return customer
