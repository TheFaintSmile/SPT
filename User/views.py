from django.shortcuts import render

# Create your views here.

def daftar_panitia (request):
    return render(request, 'daftar-panitia.html')

def login(request):
    return render(request, 'login.html')

def postSignIn(request):
	email = request.POST.get("email")
	password = request.POST.get("password")
	try:
		user = fauth.sign_in_with_email_and_password(email, password)
	except:
		return redirect(signIn)
	print(fauth.current_user)
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	return redirect('/')
