from django.shortcuts import render, redirect
from backend.crud.crud_event import event_create
import json

# Create your views here.
def create_kepanitiaan(request):
	return render(request, 'data_kepanitiaan.html')

def create_divisi(request):
	return render(request, 'data_divisi.html')

def post_create_kepanitiaan(request):
	nama = request.POST.get("nama-acara")
	deskripsi = request.POST.get("deskripsi-acara")
	tugas_umum = get_data_tugas(request, "tugas-umum")
	tugas_khusus = get_data_tugas(request, "tugas-khusus")
	mulai_event = request.POST.get("mulai-event")
	selesai_event = request.POST.get("selesai-event")
	tingkat = request.POST.get("tingkat")
	bidang = request.POST.get("bidang")
	timeline = request.POST.get("uploadFiles")
	timeline = json.loads(timeline)

	# print("Testing :\n")
	# print(request.POST.get("testing-ae-brok"))
	# print(type(request.POST.get("testing-ae-brok")))
	# print("\nSelesai Testing")
	if timeline[0]["successful"] :
		timeline_array = []
		for i in timeline[0]["successful"] :
			timeline_array.append(i["meta"]["id_firebase"])
		message = event_create(nama, deskripsi, tugas_umum, tugas_khusus, mulai_event, selesai_event, tingkat, bidang, timeline_array)

	if message == "" :
		return redirect("event_kepanitiaan:add-divisi")
	return redirect("event_kepanitiaan:create-event")

def get_data_tugas(request, jenis_tugas):
	counter = 1
	tugas_1 = request.POST.get(jenis_tugas + "-"+str(counter)) 
	arr_tugas = []

	if (tugas_1 != None):
		arr_tugas.append(tugas_1)
		counter += 1
		tugas_2 = request.POST.get(jenis_tugas + "-"+str(counter))
		while (tugas_2 != None):
			arr_tugas.append(tugas_2)
			counter += 1
			tugas_2 = request.POST.get(jenis_tugas + "-"+str(counter))
		return arr_tugas
	
	return None