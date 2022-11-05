from django.shortcuts import render, redirect
from backend.crud.crud_user_panitia import user_panitia_create, user_panitia_read, user_panitia_update_data 
from django.contrib import auth
from backend.misc import firebase_init

fauth = firebase_init

def signUp(request):
	return render(request, 'daftar-panitia.html')

def postSignUp(request):
	# idPanitia = request.POST.get("nama-acara")
	nama = request.POST.get("nama-acara")
	email = request.POST.get("email")
	kategori = request.POST.get("kategori")
	password = request.POST.get("password")
	password2 = request.POST.get("retype-password")
	photos = request.POST.get("uploadFiles")
	photos = json.loads(photos)
	
	if (password == password2):
		message = user_panitia_create(nama, email, password, kategori)
	
	if message == "":
		return redirect("user_panitia:signin")
		# mau gw tambahin else if per error dari crud_usernya
	else:
		return redirect("user_panitia:signup")

def signIn(request):
	return redirect('/user/login')

def update_data_panitia(request):
	return render(request, 'update-panitia.html')

def post_update_data_panitia(request) :
	# idPanitia = request.POST.get("nama-acara")
	nama = request.POST.get("nama-acara")
	email = request.POST.get("email")
	kategori = request.POST.get("kategori")
	# jumlah_divisi = request.POST.get("jumlah-divisi")
	local_id = request.session['user_id']
	email_lama = request.session['email']

	# Update data to firebase
	message = user_panitia_update_data(nama, email, kategori, local_id, email_lama)
	request.session['nama'] = str(nama.split(" ")[0])
	request.session['email'] = str(email)
	request.session['nama_lengkap'] = str(nama)
	
	if message == "" :
		return redirect("/")
	else :
		return redirect("user_panitia:update-data-panitia")
		