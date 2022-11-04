import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def event_create(nama, deskripsi, tugas_umum, tugas_khusus, tanggal_mulai, tanggal_selesai, tingkat, bidang, timeline) :
    
    try :
        data = {
            'nama' : nama,
            'deskripsi' : deskripsi,
            'tugas_umum' : tugas_umum,
            'tugas_khusus' : tugas_khusus,
            'tanggal_mulai' : tanggal_mulai,
            'tanggal_selesai' : tanggal_selesai,
            'tingkat' : tingkat,
            'bidang' : bidang,
            'timeline' : timeline
        }
        db.collection('events').document(nama).set(data)
        return nama
    except :
        return "terjadi error"

def event_read(namaEvent) :
    try :
        data = db.collection('events').document(namaEvent).get().to_dict()
    except :
        data = []
    print('Successfully fetched user data: {0}'.format(data))
    return data

def event_update(deskripsi, tugas_umum, tugas_khusus, tanggal_mulai, tanggal_selesai, tingkat, bidang, timeline) :
    try :
        data = {
            'nama' : nama,
            'deskripsi' : deskripsi,
            'tugas_umum' : tugas_umum,
            'tugas_khusus' : tugas_khusus,
            'tanggal_mulai' : tanggal_mulai,
            'tanggal_selesai' : tanggal_selesai,
            'tingkat' : tingkat,
            'bidang' : bidang,
            'timeline' : timeline
        }
        db.collection('events').document(nama).set(data)
    except :
        return "terjadi error"

def event_delete(namaEvent) :
    db.collection('events').document(namaEvent).delete()