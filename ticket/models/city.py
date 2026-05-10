from django.db import models
from .district import District
from .users import User

class City(models.Model):
	description = models.CharField(max_length=255,null=True)
	district = models.ForeignKey(District, on_delete=models.CASCADE,null=True) 
	created = models.DateTimeField()
	created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	is_active = models.IntegerField(default=1)
	class Meta:
		db_table = "tbl_city"


