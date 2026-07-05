from django.db import models


BUSINESS_TYPE = (
    ("saas","saas"),
    ("agency","agency"),
    ("freelance","freelance"),
    ("others","others")
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

