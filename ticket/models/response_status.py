from django.db import models
from .users import User

class ResponseStatus(models.Model):
	description = models.CharField(max_length=255,null=True)
	created = models.DateTimeField()
	created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	is_active = models.IntegerField(default=1)
	class Meta:
		db_table = "tbl_response_status"


