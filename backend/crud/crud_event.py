import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def event_create(nama, deskripsi, tugas, tanggal, jumlah_divisi, divisi, logo) :
    
    data = {
        'nama' : nama,
        'deskripsi' : deskripsi,
        'tugas' : tugas,
        'tanggal' : tanggal,
        'jumlah_divisi' : jumlah_divisi,
        'divisi' : divisi,
        'logo' : logo
    }
    db.collection('events').document(nama).set(data)

def event_read(namaEvent) :
    data = db.collection('events').document(namaEvent).get().to_dict()
    print('Successfully fetched user data: {0}'.format(data))
    return data

def event_update(nama, deskripsi, tugas, tanggal, jumlah_divisi, divisi, logo) :
    data = {
        'nama' : nama,
        'deskripsi' : deskripsi,
        'tugas' : tugas,
        'tanggal' : tanggal,
        'jumlah_divisi' : jumlah_divisi,
        'divisi' : divisi,
        'logo' : logo
    }
    db.collection('events').document(nama).set(data)

def event_delete(namaEvent) :
    db.collection('events').document(namaEvent).delete()