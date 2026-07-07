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

BILLING_STATUS = (
    ("successful","successful"),
    ("failed","failed"),
    ("pending","pending")
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


class Subscribers(models.Model):
    subscriber = models.ForeignKey("users.User",on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
    next_payment = models.DateField()
    previous_payment = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)

class BillingHistory(models.Model):
    subscriber = models.ForeignKey("users.User",on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.SET_NULL,null=True)
    amount = models.DecimalField(max_digits=40,decimal_places=2)
    status = models.CharField(max_length=20,choices=BILLING_STATUS,default="pending")

    last_updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
