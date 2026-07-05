from django.db import models
from django.utils import choices


BUSINESS_TYPE = (
    ("saas","saas"),
    ("agency","agency"),
    ("freelance","freelance"),
    ("others","others")
)

BILLING_INTERVAL = (
    ("daily","daily"),
    ("weekly","weekly"),
    ("monthly","monthly"),
    ("annually","annually"),
    ("custom","custom")
)

PLAN_STATUS = (
    ("active","active"),
    ("inactive","inactive"),
    ("archived","archived")
)




class Merchant(models.Model):
    business_name = models.CharField(max_length=250)
    business_email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    business_type = models.CharField(max_length=100,choices="")
    web_url = models.CharField(max_length=250,null=True)

    webhook_url = models.URLField(null=True)
    test_api_key = models.CharField(max_length=500)
    live_api_key = models.CharField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)


class Plan(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=40,decimal_places=2)
    billing_interval = models.CharField(max_length=100,choices=BILLING_INTERVAL)
    billing_interval_in_days = models.IntegerField(null=True)
    trial_period_in_days = models.IntegerField(null=True)
    status = models.CharField(PLAN_STATUS,max_length=100,default="active")

    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
