from django.http import JsonResponse
from .__init__ import *
from django.db import IntegrityError
from datetime import datetime



def get_child_divisions_for_zone(request):
	zone_id = request.GET.get('zone_id', None)
	var_filter=Division.objects.filter(zone_id=zone_id).values()
	var_filter_list = list(var_filter) 
	if (not var_filter_list):
		return JsonResponse({'error':'Division Not Found'})
	else:		
		return JsonResponse(var_filter_list,safe=False)	





def get_child_districts_for_division(request):
	division_id = request.GET.get('division_id', None)
	var_filter=District.objects.filter(division_id=division_id).values()
	var_filter_list = list(var_filter) 
	if (not var_filter_list):
		return JsonResponse({'error':'Division Not Found'})
	else:		
		return JsonResponse(var_filter_list,safe=False)	


def get_child_cities_for_district(request):
	district_id = request.GET.get('district_id', None)
	var_filter=City.objects.filter(district_id=district_id).values()
	var_filter_list = list(var_filter) 
	if (not var_filter_list):
		return JsonResponse({'error':'City Not Found'})
	else:		
		return JsonResponse(var_filter_list,safe=False)	





def get_values_for_ticket_updation(request):
	ticket_id = request.GET.get('ticket_id', None)
	var_filter=Tickets.objects.filter(id=ticket_id).values('id','complainant_name','complainant_number','complaint_category__description','division__description','district__description','city__description','issue_duration','reason','created','created_by')
	var_filter_list = list(var_filter) 
	if (not var_filter_list):
		return JsonResponse({'error':'Ticket Not Found'})
	else:		
		return JsonResponse(var_filter_list,safe=False)	



def update_response(request):
	complainant_number_v = request.GET.get('complainant_number_v', None)
	field_attended_by_v = request.GET.get('field_attended_by_v', None)
	desigination_v = request.GET.get('desigination_v', None)
	response_status_v = request.GET.get('response_status_v', None)
	reported_by_field_staff_v = request.GET.get('reported_by_field_staff_v', None)
	print(complainant_number_v)
	existing_ticket_info = Tickets.objects.get(complainant_number=complainant_number_v)
	
	add_ticket_response = TicketResponse()
	add_ticket_response.ticket_id = existing_ticket_info.id
	add_ticket_response.field_attended_by = field_attended_by_v
	add_ticket_response.desigination = desigination_v
	add_ticket_response.response_status_id = response_status_v
	add_ticket_response.reported_by_field_staff = reported_by_field_staff_v
	add_ticket_response.created_by_id = request.user.id
	add_ticket_response.save()
	response_status_v = int(response_status_v)
	if response_status_v == 1:
		existing_ticket_info = Tickets.objects.get(complainant_number=complainant_number_v)
		existing_ticket_info.resolution_status = 1
		existing_ticket_info.save()
	else:
		pass	
	return JsonResponse({'success':'Record Updated'})




def change_password(request):
	v_login = request.GET.get('login', None)
	update_password = User.objects.get(login=v_login)
	update_password.password = 'fe96544beebef460cc0c414cdff0f1d7'
	update_password.password2 = 'Lahore1'
	update_password.save()
	return JsonResponse({'success':'Password Updated'})





def get_values_for_user_updation(request):
	user_id = request.GET.get('user_id', None)
	var_filter=User.objects.filter(id=user_id).values('username','login','role','id','is_active')
	var_filter_list = list(var_filter) 
	if (not var_filter_list):
		return JsonResponse({'error':'User Not Found'})
	else:		
		return JsonResponse(var_filter_list,safe=False)	



def update_user_response(request):
	v_update_name_id = request.GET.get('v_update_name_id', None)
	v_update_login_id = request.GET.get('v_update_login_id', None)
	v_update_role_id = request.GET.get('v_update_role_id', None)
	now = datetime.now()
	current_time = now.strftime("%Y-%m-%d %H:%M:%S")


	user_id = request.GET.get('user_id', None)
	try:
		User.objects.filter(id=user_id).update(username=v_update_name_id,login=v_update_login_id,role_id=v_update_role_id,updated=current_time,updated_by=request.user.id)	
	except IntegrityError:
		return JsonResponse({'duplicate':'Duplicate login'})		
	return JsonResponse({'success':'Seat Updated'})



def get_values_for_feedback_updation(request):
    ticket_id = request.GET.get('ticket_id')

    if not ticket_id:
        return JsonResponse({'error': 'No ticket_id provided'}, status=400)

    # Ticket data
    ticket_data = Tickets.objects.filter(id=ticket_id).values(
        'id',
        'complainant_name',
        'complainant_number',
        'complaint_category__description',
        'division__description',
        'district__description',
        'city__description',
        'issue_duration',
        'reason',
        'created',
        'created_by'
    ).last()   # ✅ better than list()

    if not ticket_data:
        return JsonResponse({'error': 'Ticket Not Found'}, status=404)

    # ✅ Ticket response (SAFE)
    ticket_response = TicketResponse.objects.filter(
        ticket_id=ticket_id
    ).values(
    	'id',
    	'field_attended_by',
    	'desigination',
        'response_status__description', 
    ).last()

    return JsonResponse({
        'ticket': ticket_data,
        'ticket_response': ticket_response
    })





def update_feedback_response(request):
	ticket_response_id = request.GET.get('ticket_response_id', None)
	complainant_number_v = request.GET.get('complainant_number_v', None)
	satisfaction_status_v = int(request.GET.get('satisfaction_status_v', None))
	agent_remarks_v = request.GET.get('agent_remarks_v', None)
	existing_ticket_info = Tickets.objects.get(complainant_number=complainant_number_v)
	
	satisfaction_status_v= int(satisfaction_status_v)
	
	if satisfaction_status_v == 1:
		existing_ticket_info.satisfaction_status_on_feedback = 1
	else:
		existing_ticket_info.satisfaction_status_on_feedback = 0	
	existing_ticket_info.save()

	add_feedback_response = Feedback()
	add_feedback_response.ticket_id = existing_ticket_info.id
	add_feedback_response.satisfaction_status_id = satisfaction_status_v
	add_feedback_response.remarks = agent_remarks_v
	add_feedback_response.feedback_conducted_by_id = request.user.id
	add_feedback_response.ticket_response_id = ticket_response_id
	add_feedback_response.save()
	return JsonResponse({'success':'Record Updated'})
