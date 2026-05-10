from django.db import models
from .users import User
from .categories import Categories
from .zone import Zone
from .division import Division
from .district import District
from .city import City
from .ticket_status import TicketStatus
from .satisfaction_status import SatisfactionStatus

class Tickets(models.Model):
    complainant_name = models.CharField(max_length=255,null=True)
    complainant_number = models.CharField(max_length=255,null=True,unique=True)
    complaint_category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE,null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=True)
    issue_duration = models.IntegerField(default=0)
    reason = models.TextField(null=True)
    # ticket_status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    resolution_status = models.IntegerField(default=0)
    plant_address = models.CharField(max_length=255,null=True)
    code = models.CharField(max_length=255,null=True)
    satisfaction_status_on_feedback = models.IntegerField(null=True)
    class Meta:
        db_table = 'tbl_tickets'