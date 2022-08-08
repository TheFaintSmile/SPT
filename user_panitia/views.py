from django.shortcuts import render, redirect
from backend.crud.crud_user_panitia import user_panitia_create, user_panitia_read, user_panitia_update_data 
from django.contrib import auth
from backend.misc import firebase_init

fauth = firebase_init

def signUp(request):
	return render(request, 'daftar-panitia.html')

def postSignUp(request):
	idPanitia = request.POST.get("nama-acara")
	nama = request.POST.get("nama-acara")
	email = request.POST.get("email")
	password = request.POST.get("password")
	password2 = request.POST.get("retype-password")
	kategori = request.POST.get("kategori")
	jumlah_divisi = request.POST.get("jumlah-divisi")
	
	if (password == password2):
		message = user_panitia_create(idPanitia, nama, email, password, kategori, jumlah_divisi)
	
	if message == "":
		return redirect("user_panitia:signin")
	else:
		return redirect("user_panitia:signup")

def signIn(request):
	return redirect('/user/login')

def update_data_panitia(request):
	return render(request, 'update-panitia.html')

def post_update_data_panitia(request) :
	idPanitia = request.POST.get("nama-acara")
	nama = request.POST.get("nama-acara")
	email = request.POST.get("email")
	kategori = request.POST.get("kategori")
	jumlah_divisi = request.POST.get("jumlah-divisi")
	id_lama = request.session['user_id']

	# Update data to firebase
	if photos[0]["successful"] :
		pas_foto = []
		for i in photos[0]["successful"] :
			pas_foto.append(i["meta"]["id_firebase"])
		message = user_panitia_update_data(idPanitia, nama, email, kategori, jumlah_divisi, id_lama)
		
		if message == "" :
			return redirect("/")
		else :
			return redirect("user_panitia:update-data-peserta")