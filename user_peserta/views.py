from django.shortcuts import render, redirect
from backend.crud.crud_user_peserta import user_peserta_create
from django.contrib import auth
from backend.misc import firebase_init
from backend.constants.fakultas import fakultas
from backend.constants.jurusan import jurusan
import json

fauth = firebase_init.firebaseInit().auth()

def signUp(request):
	return render(request, 'daftar-peserta.html')

def postSignUp(request):
	idPeserta = request.POST.get("nama_lengkap")
	nama = request.POST.get("nama_lengkap")
	fakultas = request.POST.get("fakultas")
	jurusan = request.POST.get("jurusan")
	email = request.POST.get("email")
	npm = request.POST.get("npm")
	password = request.POST.get("password")
	password2 = request.POST.get("retype-password")
	photos = request.POST.get("uploadFiles")
	photos = json.loads(photos)
	
	if (password == password2):
		# Upload data to firebase
		if photos[0]["successful"] :
			pas_foto = []
			for i in photos[0]["successful"] :
				pas_foto.append(i["meta"]["id_firebase"])
			message = user_peserta_create(idPeserta, email, password, nama, fakultas, jurusan, npm, pas_foto)
			# Sign Up User
			if message == "" :
				return redirect("user_peserta:signin")
			else :
				return redirect("user_peserta:signup")

def signIn(request):
	return redirect('user/login')

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

def logout(request):
	auth.logout(request)
	return redirect("user_peserta:signin")

