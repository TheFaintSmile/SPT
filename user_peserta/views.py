from django.shortcuts import render, redirect
from backend.CRUD.crud_user_peserta import user_peserta_create
from django.contrib import auth
from backend.misc import firebase_init
from backend.constants.fakultas import fakultas
from backend.constants.jurusan import jurusan
import json

fauth = firebase_init.firebaseInit().auth()

def signUp(request):
	return render(request, 'signUp.html', {
		"pi": pi,
		"birdeptim": birdeptim,
		"kode_fungsionaris": kode_fungsionaris
	})

def postSignUp(request):
	idPeserta = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password1")
	password2 = request.POST.get("password2")
	nama = request.POST.get("nama")
	fakultas = request.POST.get("fakultas")
	jurusan = request.POST.get("jurusan")
	npm = request.POST.get("npm")
	photos = request.POST.get("uploadFiles")
	photos = json.loads(photos)
	
	if (password == password2):
		if photos[0]["successful"]:
        	pas_foto = []
        	for i in photos[0]["successful"]:
            	pas_foto.append(i["meta"]["id_firebase"])
        	# message = kr_create(request, judul, nama_kegiatan, deskripsi, norek, anrek, voucher, nominal, photos_meta)
			message = user_peserta_create(idPeserta, email, password, nama, fakultas, jurusan, npm, pas_foto)
        	if message != "there is error":
            	# return redirect("/reimbursement/detail/" + message)
				return redirect("user:signin")
        	else:
            	message = "Gagal Upload"
            	return redirect("user:signup")
    	else:
        	message = "Gagal Upload"
        	return redirect("user:signup")
		
	if message == "":
		return redirect("user:signin")
	else:
		return redirect("user:signup")

def signIn(request):
	return render(request, 'signIn.html')

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
	return redirect("user:signin")

