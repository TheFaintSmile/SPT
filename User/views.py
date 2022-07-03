from django.shortcuts import render

# Create your views here.
def daftar_peserta (request):
    return render(request, 'daftar-peserta.html')

def daftar_panitia (request):
    return render(request, 'daftar-panitia.html')

def login(request):
    return render(request, 'login.html')
