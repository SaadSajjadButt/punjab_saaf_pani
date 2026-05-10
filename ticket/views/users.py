from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .__init__ import *
from django.db import IntegrityError
from datetime import datetime
import socket





def display_users(request):
	if request.session.has_key('is_logged'):
		if request.method=='POST':
			select_type_user = request.POST.get('select_type_user',False)
			if select_type_user == "All":
				all_users = User.objects.all()
			else:
				login_for_user = request.POST.get('login_for_user',False)
				all_users = User.objects.filter(login=login_for_user)	 
			all_roles = Role.objects.all()
			return render(request,'ticket/display_users.html',{'all_users':all_users,'all_roles':all_roles})
		else:
			all_roles = Role.objects.all()
			all_users = User.objects.all()
			return render(request,'ticket/display_users.html',{'all_users':all_users,'all_roles':all_roles})
	else:
		return redirect('login')




def display_add_user(request):
	if request.session.has_key('is_logged'):
		all_roles = Role.objects.all()
		return render(request,'ticket/display_add_user.html',{'all_roles':all_roles})
	else:
		return redirect('login')




def add_users(request):
	if request.session.has_key('is_logged'):
		if request.method=='POST':
			if request.POST['password1']==request.POST['password2']:
				try:
					user=User.objects.get(login=request.POST['login'])
					return render(request,'ticket/display_add_user.html',{'error':'Login ID is already taken','all_roles':Role.objects.all(),'users':User.objects.all()})
				except User.DoesNotExist:	
					user=User.objects.create_user(username=request.POST['name'] , password=request.POST['password1'],password2=request.POST['password1'], role_id=request.POST['role_id'] ,login=request.POST['login'],email=request.POST['email'],created_by=request.user.id)
					#auth.login(request,user )
					request.session['is_logged']=True
					return render(request,'ticket/display_add_user.html',{'success':'User Successfully Created','all_roles':Role.objects.all(),'users':User.objects.all()})
			else:
				return render(request,'ticket/display_add_user.html',{'error':'Password does not matched','all_roles':Role.objects.all(),'users':User.objects.all()})
		else:
			return render(request,'ticket/display_add_user.html',{'all_roles':Role.objects.all(),'users':User.objects.all()})
	else:
		auth.logout(request)
		return redirect('login')		
