from django.db import models
from django.contrib.auth.models import AbstractUser



USER_TYPES = (
    ("system_admin","system_admin"),
    ("tenant_admin","tenant_admin"),
    ("customer","customer")
)


class User(AbstractUser):
    user_type = models.CharField(choices=USER_TYPES,max_length=100)
