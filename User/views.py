from django.shortcuts import render, redirect
from django.contrib import auth
from backend.misc import firebase_init, cekEmailVerified, getUserRole
from backend.crud import crud_user_peserta, crud_user_panitia

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
	
	session_id = user['idToken']

	request.session['user_id'] = str(user['localId'])					# user_id is the same as id in firebase collection
	request.session['uid'] = str(session_id)
	request.session['nama'] = str(user['localId'].split(' ')[0])
	request.session['isPanitia'] = getUserRole.getUserRole(request)
	
	print(request.session['isPanitia'])
	
	if(cekEmailVerified.cekEmailVerified(request) == False):
		return redirect("/user/email-verify")
	return redirect('/')

def logout(request):
	auth.logout(request)
	return redirect("/user/login")

def post_email_verify(request):
	try :
		fauth.send_email_verification_link(request.session['uid'])
	except :
		print("gagal")
		return redirect("/user/email-verify")
	return redirect("/")

def email_verify(request):
	return render(request, 'email_verify.html')

def change_password(request):
	return render(request, 'change-password.html')

def post_change_password(request):
	# old_password = request.POST.get("old-password")
	new_password = request.POST.get("new-password")
	retype_new_password = request.POST.get("retype-new-password")

	if(new_password == retype_new_password):
		if (request.session['isPanitia']):
			crud_user_panitia.user_panitia_update_password(request.session['user_id'], new_password)
		else :
			crud_user_peserta.user_peserta_update_password(request.session['user_id'], new_password)
		return redirect('/')
	
	return render(request, 'change-password.html')
