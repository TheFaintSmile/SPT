from django.shortcuts import render
# from backend.crud.crud_event import event_create, event_read, event_update_data, event_delete_data

# Create your views here.
def create_kepanitiaan(request):
	return render(request, 'data_kepanitiaan.html')

def create_divisi(request):
	return render(request, 'data_divisi.html')

# def post_create_kepanitiaan(request):
# 	nama = request.POST.get("nama-acara")
# 	deskripsi = request.POST.get("deskripsi-acara")
# 	# tugas umum
# 	# tugas khusus
# 	mulai_event = request.POST.get("mulai-event")
# 	selesai_event = request.POST.get("selesai-event")
# 	tingkat = request.POST.get("tingkat")
# 	bidang = request.POST.get("bidang")
# 	timeline = request.POST.get("timeline")
	
	
# 	# return redirect("event_kepanitiaan:create-kepanitiaan")