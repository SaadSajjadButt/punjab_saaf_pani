from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .__init__ import *
from django.db import IntegrityError
from datetime import datetime,date
from django.utils import timezone



def filterfeedbacks(request):
	if not request.session.has_key('is_logged'):
		auth.logout(request)
		return redirect('login')


	today = date.today()
	start_of_month = today.replace(day=1)

	# Defaults
	start_date = start_of_month
	end_date = today
	selected_status = 0

	# Base queryset
	tickets_qs = Tickets.objects.all()

	if request.method == 'POST':
		start_date = datetime.strptime(request.POST.get('start'), "%Y-%m-%d").date()
		end_date = datetime.strptime(request.POST.get('end'), "%Y-%m-%d").date()
		selected_status = int(request.POST.get('status'))

	# Apply date filter
	tickets_qs = tickets_qs.filter(created__date__range=[start_date, end_date])

	# Apply status filter
	if selected_status == 0:
		tickets_qs = tickets_qs.filter(resolution_status=1)
	elif selected_status == 1:
		tickets_qs = tickets_qs.filter(resolution_status=1,satisfaction_status_on_feedback=1)
	elif selected_status == 2:
		tickets_qs = tickets_qs.filter(resolution_status=1,satisfaction_status_on_feedback=0)
	elif selected_status == 3:
		tickets_qs = tickets_qs.filter(resolution_status=1,satisfaction_status_on_feedback__isnull=True)	    
	# 2 = all (no filter)	

	tickets_qs = tickets_qs.order_by('-id')

	all_satisfaction_responses = SatisfactionStatus.objects.all()

	ticket_list = []


	context = {
		'tickets': tickets_qs,
		'all_satisfaction_responses':all_satisfaction_responses,
		'start_date': start_date,
		'end_date': end_date,
		'selected_status': selected_status
	}

	return render(request, 'ticket/feedback.html', context)
