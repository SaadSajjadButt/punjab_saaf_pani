from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .__init__ import *
import tablib
from django.db.models import F
from dateutil import parser
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime




def display_report_ticket(request):
	if request.session.has_key('is_logged'):
		return render(request,'ticket/display_report.html',{})
	else:
		return redirect('login')




def export_report_ticket(request):

    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    # Convert to datetime
    if from_date and to_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")

    # Optimized query
    tickets = Tickets.objects.select_related(
        'complaint_category',
        'division',
        'district',
        'city',
        'created_by'
    ).prefetch_related(
        'ticketresponse_set',
        'feedback_set'
    )

    # Apply date filter
    if from_date and to_date:
        tickets = tickets.filter(created__date__range=[from_date, to_date])

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Tickets Report"

    # Header Row
    ws.append([
        'Ticket ID',
        'Code',
        'Complainant Name',
        'Complainant Number',
        'Category',
        'Division',
        'District',
        'City',
        'Plant Address',
        'Issue Duration',
        'Reason',
        'Created Date',
        'Created By',
        'Resolution Status',

        # Ticket Response
        'Field Attended By',
        'Designation',
        'Response Status',
        'Reported By Field Staff',
        'Response Date',

        # Feedback
        'Feedback Remarks',
        'Feedback By',
        'Satisfaction Status',
        'Feedback Date'
    ])

    # Data Rows
    for t in tickets:

        # Get latest response (important)
        response = t.ticketresponse_set.order_by('-id').first()

        # Get latest feedback
        feedback = t.feedback_set.order_by('-id').first()

        ws.append([
            t.id,
            t.code,
            t.complainant_name,
            t.complainant_number,
            t.complaint_category.description if t.complaint_category else '',
            t.division.description if t.division else '',
            t.district.description if t.district else '',
            t.city.description if t.city else '',
            t.plant_address,
            t.issue_duration,
            t.reason,
            t.created.strftime('%Y-%m-%d %H:%M') if t.created else '',
            t.created_by.username if t.created_by else '',
            t.resolution_status,

            # Response
            response.field_attended_by if response else '',
            response.desigination if response else '',
            response.response_status.description if response and response.response_status else '',
            response.reported_by_field_staff if response else '',
            response.response_added_at.strftime('%Y-%m-%d %H:%M') if response and response.response_added_at else '',

            # Feedback
            feedback.remarks if feedback else '',
            feedback.feedback_conducted_by.username if feedback and feedback.feedback_conducted_by else '',
            feedback.satisfaction_status.description if feedback and feedback.satisfaction_status else '',
            feedback.feedback_conducted_at.strftime('%Y-%m-%d %H:%M') if feedback and feedback.feedback_conducted_at else '',
        ])

    # Response setup
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="tickets_report.xlsx"'

    wb.save(response)
    return response