from django.shortcuts import render, redirect
from backend.crud.crud_user_panitia import user_panitia_create 
from django.contrib import auth
from backend.misc import firebase_init

def dashboard(request):
	return render(request, 'dashboard-panitia.html')

