from django.shortcuts import render, redirect
from backend.crud.crud_user_panitia import user_panitia_create 
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
		print("test daftar panitia")
	if message == "":
		return redirect("user_panitia:signin")
	else:
		return redirect("user_panitia:signup")

def signIn(request):
	return redirect('/user/login')

def logout(request):
	auth.logout(request)
	return redirect("user_panitia:signin")

