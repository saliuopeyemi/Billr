from django.db import models


class Tenant(models.Model):
    business_name = models.CharField(max_length=250)
    business_email = models.EmailField()
