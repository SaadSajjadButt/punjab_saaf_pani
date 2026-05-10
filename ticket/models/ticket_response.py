from django.db import models
from .users import User
from .ticket import Tickets
from .response_status import ResponseStatus

class TicketResponse(models.Model):
	ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE,null=True)
	field_attended_by = models.CharField(max_length=255,null=True)
	desigination = models.CharField(max_length=255,null=True)
	response_status = models.ForeignKey(ResponseStatus, on_delete=models.CASCADE,null=True)
	reported_by_field_staff = models.CharField(max_length=255,null=True)
	response_added_at = models.DateTimeField(null=True,auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	is_active = models.IntegerField(default=1)
	class Meta:
		db_table = "tbl_ticket_reponse"



