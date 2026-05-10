from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .__init__ import *
from django.db import IntegrityError
from datetime import datetime,date
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.functions import Now


def filtertickets(request):
    if not request.session.has_key('is_logged'):
        auth.logout(request)
        return redirect('login')

    all_responses = ResponseStatus.objects.all()

    today = date.today()
    start_of_month = today.replace(day=1)

    # Defaults
    start_date = start_of_month
    end_date = today
    selected_status = 0

    # Base queryset
    if request.user.zone_id == 1:
        tickets_qs = Tickets.objects.filter(division__zone=1)
    elif request.user.zone_id == 2:    
        tickets_qs = Tickets.objects.filter(division__zone=2)
    elif request.user.zone_id == 3:
        tickets_qs = Tickets.objects.filter(division__zone=3)    
    else:    
        tickets_qs = Tickets.objects.all()

    if request.method == 'POST':
        start_date = datetime.strptime(request.POST.get('start'), "%Y-%m-%d").date()
        end_date = datetime.strptime(request.POST.get('end'), "%Y-%m-%d").date()
        selected_status = int(request.POST.get('status'))

    # Apply date filter
    tickets_qs = tickets_qs.filter(created__date__range=[start_date, end_date])

    # Apply status filter
    if selected_status == 0:
        tickets_qs = tickets_qs.filter(resolution_status=0)
    elif selected_status == 1:
        tickets_qs = tickets_qs.filter(resolution_status=1)
    # 2 = all (no filter)

    tickets_qs = tickets_qs.order_by('-id')

    # ✅ Dashboard counts
    total_tickets = tickets_qs.count()
    pending = tickets_qs.filter(resolution_status=0).count()
    resolved = tickets_qs.filter(resolution_status=1).count()
    critical = tickets_qs.filter(resolution_status=0,created__lt=Now() - timedelta(days=7)).count()
    # Aging calculation
    now = timezone.now()
    ticket_list = []
 

    for ticket in tickets_qs:
        aging = now - ticket.created
        days = aging.days
        hours = aging.seconds // 3600
        minutes = (aging.seconds % 3600) // 60

        aging_str = f"{days}d {hours}h {minutes}m"

        # ✅ Correct color logic
        if days >= 7:
            color = 'red'
        elif days >= 2:
            color = 'orange'
        elif days < 2:
            color = 'yellow'
               
        ticket_list.append({
            'ticket': ticket,
            'aging': aging_str,
            'color': color,
            'days': days
        })

    context = {
        'tickets': ticket_list,
        'all_responses': all_responses,
        'start_date': start_date,
        'end_date': end_date,
        'selected_status': selected_status,

        # Dashboard data
        'total_tickets': total_tickets,
        'pending': pending,
        'resolved': resolved,
        'critical': critical
    }

    return render(request, 'ticket/display_tickets.html', context)

	


# def filtertickets(request):
# 	if request.session.has_key('is_logged'):
# 		all_responses = ResponseStatus.objects.all()
# 		if request.method=='POST':
# 			start_date = request.POST['start']
# 			end_date = request.POST['end']
# 			status =  int(request.POST['status'])
# 			if status == 2:
# 				tickets = Tickets.objects.filter(created__date__range=[start_date, end_date]).order_by('-id')
# 			elif status == 0:
# 				tickets = Tickets.objects.filter(created__date__range=[start_date, end_date],resolution_status=0).order_by('-id')
# 			elif status == 1:
# 				tickets = Tickets.objects.filter(created__date__range=[start_date, end_date],resolution_status=1).order_by('-id')	
			
# 			return render(request,'ticket/display_tickets.html',{'tickets':tickets,'all_responses':all_responses})		
# 		else:
# 			today = date.today()
# 			tickets = Tickets.objects.filter(created__date__range=[today, today],resolution_status=0).order_by('-id')
# 			return render(request,'ticket/display_tickets.html',{'tickets':tickets,'all_responses':all_responses})		
# 	else:
# 		auth.logout(request)
# 		return redirect('login')




def launchtickets(request):
	if request.session.has_key('is_logged'):
		if request.method=='POST':
			return render(request,'ticket/launch_ticket.html',{'Division':Division.objects.all(),'Categories':Categories.objects.all(),'Ticketstatus':TicketStatus.objects.all(),'Zone': Zone.objects.all()})
		else:
			return render(request,'ticket/launch_ticket.html',{'Division':Division.objects.all(),'Categories':Categories.objects.all(),'Ticketstatus':TicketStatus.objects.all(),'Zone': Zone.objects.all()})	
	else:
		auth.logout(request)
		return redirect('login')		




def addtickets(request):
    if request.session.has_key('is_logged'):
        # Prepare context data to avoid repetition
        context = {
            'Zone': Zone.objects.all(),
            'Division': Division.objects.all(),
            'Categories': Categories.objects.all(),
            'Ticketstatus': TicketStatus.objects.all()
        }

        if request.method == 'POST':
            try:
                add_ticket = Tickets()
                add_ticket.complainant_name = request.POST['complainant_name']
                add_ticket.complainant_number = request.POST['complainant_number']
                add_ticket.complaint_category_id = request.POST['complaint_category']
                add_ticket.zone_id = request.POST['zone_id']
                add_ticket.division_id = request.POST['division_id']
                add_ticket.district_id = request.POST['district_id']
                add_ticket.city_id = request.POST['city_id']
                add_ticket.issue_duration = request.POST['duration_since_issue']
                add_ticket.reason = request.POST['reason_id']
                add_ticket.plant_address = request.POST['plant_address']
                add_ticket.code = request.POST['code']
                add_ticket.created_by_id = request.user.id
                add_ticket.save() 
                
                context['ticket_success'] = 'ticket_success'
                return render(request, 'ticket/launch_ticket.html', context)

            except IntegrityError:
                # This catches the unique constraint violation
                context['error_message'] = "This complainant number already exists."
                return render(request, 'ticket/launch_ticket.html', context)
        
        return render(request, 'ticket/launch_ticket.html', context)
    
    else:
        auth.logout(request)
        return redirect('login')




