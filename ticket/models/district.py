from django.db import models
from .division import Division
from .users import User

class District(models.Model):
	description = models.CharField(max_length=255,null=True)
	division = models.ForeignKey(Division, on_delete=models.CASCADE,null=True) 
	created = models.DateTimeField()
	created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	is_active = models.IntegerField(default=1)
	class Meta:
		db_table = "tbl_district"


