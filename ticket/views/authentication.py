from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .__init__ import *
import hashlib



def login(request):
    if request.method == 'POST':
        login_value = request.POST['login']
        password = request.POST['password']   ### Testing comments

        user = auth.authenticate(login=login_value, password=password)

        if user is not None:
            # ✅ correct credentials
            if user.is_active:
                auth.login(request, user)
                request.session['is_logged'] = True
                return redirect('home')
            else:
                return render(request, 'ticket/login.html', {
                    'account_deactivation': 'Your account is deactivated'
                })

        else:
            # 🔍 Check if user exists but is inactive
            user_obj = User.objects.filter(login=login_value).first()

            if user_obj and not user_obj.is_active:
                return render(request, 'ticket/login.html', {'account_deactivation': 'Your account is deactivated'})

            return render(request, 'ticket/login.html', {'error': 'Username or Password is incorrect!!!'})

    return render(request, 'ticket/login.html')




def logout(request):
	if request.method=='GET':
		auth.logout(request)
		return redirect('login')
	else:
		return render(request,'ticket/login.html')


def password_reset(request):
	if request.session.has_key('is_logged'):
		if request.method=='POST':
			old_password = request.POST['old_password']
			my_string = request.POST['password1']
			my_string_md5 = (hashlib.md5(my_string.encode('utf-8')).hexdigest())
			old_password_md5 = (hashlib.md5(old_password.encode('utf-8')).hexdigest())
			check_old_password = User.objects.get(id=request.user.id) 
			if check_old_password.password == old_password_md5:
				if request.POST['password1'] == request.POST['password2']:
					update_user_password = User.objects.get(id=request.user.id) 
					update_user_password.password = my_string_md5
					update_user_password.password2 = my_string
					update_user_password.save()
					return render(request,'ticket/display_password_reset.html',{'success':'success'})
				else:
					return render(request,'ticket/display_password_reset.html',{'missmatch':'missmatch'})
			else:
				return render(request,'ticket/display_password_reset.html',{'incorrect':'incorrect'})	
		else:
			return render(request,'ticket/display_password_reset.html',{})	
	else:
		auth.logout(request)
		return redirect('login')	



