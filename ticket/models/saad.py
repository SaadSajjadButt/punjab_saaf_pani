from django.db import models
# from .users import User


class Saad(models.Model):
	role_title = models.CharField(max_length=255,null=True)
	role_description = models.TextField(null=True)
	created = models.DateTimeField(null=True)
	# created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	created_by = models.CharField(max_length=255,null=True)
	is_active = models.IntegerField(default=1)
	class Meta:
		db_table = "tbl_role"


