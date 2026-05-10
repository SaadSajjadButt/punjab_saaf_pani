from django.db import models
from django.contrib.auth.models import AbstractUser
from .role import Role


class User(AbstractUser):
    class Meta:
        db_table = "tbl_users"
    login = models.CharField(unique=True,max_length=255,null=True)        
    password = models.CharField(max_length=255,null=True)
    password2 = models.CharField(max_length=255,null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,null=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_by = models.CharField(max_length=255,null=True)
    updated = models.CharField(max_length=255,null=True)
    updated_by = models.CharField(max_length=255,null=True)
    zone_id = models.IntegerField(default=0)
    USERNAME_FIELD = 'login'


