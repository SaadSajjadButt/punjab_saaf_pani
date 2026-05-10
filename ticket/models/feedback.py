from django.db import models
from .users import User
from .ticket import Tickets
from .response_status import ResponseStatus
from .satisfaction_status import SatisfactionStatus
from .ticket_response import TicketResponse

class Feedback(models.Model):
	ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE,null=True)
	remarks = models.TextField(null = True)
	feedback_conducted_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	satisfaction_status = models.ForeignKey(SatisfactionStatus, on_delete=models.CASCADE,null=True)
	ticket_response = models.ForeignKey(TicketResponse, on_delete=models.CASCADE,null=True)
	feedback_conducted_at = models.DateTimeField(null=True,auto_now_add=True)
	class Meta:
		db_table = "tbl_feedback"
