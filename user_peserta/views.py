from email import message
from django.shortcuts import render, redirect
from backend.crud.crud_user_peserta import user_peserta_create, user_peserta_update_data, user_peserta_read
from django.contrib import auth
from backend.misc import firebase_init, delFiles
import json

fauth = firebase_init

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
	return redirect('/user/login')

def update_data_peserta(request):
	return render(request, 'update-data.html')

def post_update_data_peserta(request):
	idPeserta = request.POST.get("nama_lengkap")
	nama = request.POST.get("nama_lengkap")
	fakultas = request.POST.get("fakultas")
	jurusan = request.POST.get("jurusan")
	email = request.POST.get("email")
	npm = request.POST.get("npm")
	photos = request.POST.get("uploadFiles")
	photos = json.loads(photos)
	id_lama = request.session['user_id']
	del_photo = user_peserta_read(idPeserta)["pas_foto"]

	# Update data to firebase
	if photos[0]["successful"] :
		pas_foto = []
		for i in photos[0]["successful"] :
			pas_foto.append(i["meta"]["id_firebase"])
		message = user_peserta_update_data(idPeserta, email, nama, fakultas, jurusan, npm, pas_foto, id_lama)
		
		for photo in del_photo :
			delFiles.delPhoto(photo)
		
		if message == "" :
			return redirect("/")
		else :
			return redirect("user_peserta:update-data-peserta")
