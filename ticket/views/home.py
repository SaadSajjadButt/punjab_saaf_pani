from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .__init__ import *
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db.models.functions import Now

def home(request):
	if request.session.has_key('is_logged'):
		users=User.objects.all() 
		return render(request,'ticket/home.html',{'users':users})
	else:
		return redirect('login')


# def dashboard(request):
# 	if request.session.has_key('is_logged'):
# 		return render(request,'ticket/dashboard.html',{})
# 	else:
# 		return redirect('login')



def dashboard(request):
    # ----------------- Date filter -----------------
    today = now().date()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    else:
        # Default MTD (Month to Date)
        start = today.replace(day=1)
        end = today + timedelta(days=1)
        start_date = start.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

    tickets_qs = Tickets.objects.filter(created__range=[start, end])

    # ----------------- Top stats -----------------
    stats = [
        {'title':'Total Tickets', 'count':tickets_qs.count(), "bg_class": "bg-blue", "icon": "fas fa-ticket-alt"},
        {'title':'Pending Tickets', 'count':tickets_qs.filter(resolution_status=0).count(),  "bg_class": "bg-orange", "icon": "fas fa-clock"},
        {'title':'Resolved Tickets', 'count':tickets_qs.filter(resolution_status=1).count(), "bg_class": "bg-green", "icon": "fas fa-check-circle"},
    	{'title': 'Critical Tickets', 'count': tickets_qs.filter(resolution_status=0,created__lt=Now() - timedelta(days=7)).count(),"bg_class": "bg-red", "icon": "fas fa-exclamation-triangle"}
    ]



    # ----------------- Zone → Division Drilldown -----------------
    zones = Zone.objects.filter(is_active=1)
    zone_labels, zone_data, division_drill_labels, division_drill_data = [], [], [], []

    for zone in zones:
        zone_labels.append(zone.description)
        zone_count = tickets_qs.filter(division__zone=zone).count()
        zone_data.append(zone_count)

        div_labels, div_counts = [], []
        divisions = Division.objects.filter(zone=zone, is_active=1)
        for div in divisions:
            div_labels.append(div.description)
            div_counts.append(tickets_qs.filter(division=div).count())
        division_drill_labels.append(div_labels)
        division_drill_data.append(div_counts)

    # ----------------- District → City Drilldown -----------------
    districts = District.objects.filter(is_active=1)
    district_labels, district_data, city_drill_labels, city_drill_data = [], [], [], []

    for dist in districts:
        district_labels.append(dist.description)
        dist_count = tickets_qs.filter(district=dist).count()
        district_data.append(dist_count)

        city_labels, city_counts = [], []
        cities = City.objects.filter(district=dist, is_active=1)
        for city in cities:
            city_labels.append(city.description)
            city_counts.append(tickets_qs.filter(city=city).count())
        city_drill_labels.append(city_labels)
        city_drill_data.append(city_counts)

    # ----------------- Categories Pie -----------------
    categories = Categories.objects.filter(is_active=1)
    category_labels, category_data = [], []
    for cat in categories:
        category_labels.append(cat.description)
        category_data.append(tickets_qs.filter(complaint_category=cat).count())

    # ----------------- Feedback Doughnut -----------------
    satisfaction_statuses = SatisfactionStatus.objects.filter(is_active=1)
    feedback_data = []
    for status in satisfaction_statuses:
        feedback_data.append(
            Feedback.objects.filter(ticket__in=tickets_qs, satisfaction_status=status).count()
        )

    # ----------------- Datewise Resolved Tickets Line Chart -----------------
    resolved_qs = tickets_qs.filter(resolution_status=1)
    date_labels, date_counts = [], []
    cursor = start
    while cursor < end:
        date_labels.append(cursor.strftime('%Y-%m-%d'))
        date_counts.append(resolved_qs.filter(created__date=cursor).count())
        cursor += timedelta(days=1)

    context = {
        'stats': stats,
        'zone_labels': zone_labels,
        'zone_data': zone_data,
        'division_drill_labels': division_drill_labels,
        'division_drill_data': division_drill_data,
        'district_labels': district_labels,
        'district_data': district_data,
        'city_drill_labels': city_drill_labels,
        'city_drill_data': city_drill_data,
        'category_labels': category_labels,
        'category_data': category_data,
        'feedback_data': feedback_data,
        'resolved_dates': date_labels,
        'resolved_counts': date_counts,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'ticket/dashboard.html', context)



def dash_view(request):
    return render(request, 'ticket/dash.html')