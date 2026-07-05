from django.db import models
from django.contrib.auth.models import AbstractUser



USER_TYPES = (
    ("system_admin","system_admin"),
    ("merchant_admin","merchant_admin"),
    ("customer","customer")
)


class User(AbstractUser):
    full_name = models.CharField(max_length=250)
    user_type = models.CharField(choices=USER_TYPES,max_length=100)
    related_merchant = models.ForeignKey("merchants.Merchant",on_delete=models.CASCADE,null=True)

    is_2fa_enabled = models.BooleanField(default=True)

class LoginOtp(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
