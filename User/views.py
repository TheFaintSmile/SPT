from django.shortcuts import render, redirect
from django.contrib import auth
from backend.misc import firebase_init

fauth = firebase_init
# Create your views here.

def login(request):
    return render(request, 'login.html')

def postSignIn(request):
	email = request.POST.get("email")
	password = request.POST.get("password")
	try:
		user = fauth.sign_in_with_email_and_password(email, password)
	except:
		return redirect(login)
	print(user)
	print("berhasil login")
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	return redirect('/')
