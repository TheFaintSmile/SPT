from django.shortcuts import render

# Create your views here.
def data_kepanitiaan(request):
	return render(request, 'data_kepanitiaan.html')
def data_divisi(request):
	return render(request, 'data_divisi.html')