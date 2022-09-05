import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def event_create(nama, email,deskripsi, tugas, tanggal, divisi) :
    
    data = {
        'nama' : nama,
        'email' : email,
        'deskripsi' : deskripsi,
        'tugas' : tugas,
        'tanggal' : tanggal,
        'divisi' : divisi
    }
    db.collection('events').document(email).set(data)

def event_read(emailEvent) :
    data = db.collection('events').document(emailEvent).get().to_dict()
    print('Successfully fetched user data: {0}'.format(data))
    return data

def event_update(emailEvent, nama, deskripsi, tugas, tanggal, divisi) :
    data = {
        'nama' : nama,
        'deskripsi' : deskripsi,
        'tugas' : tugas,
        'tanggal' : tanggal,
        'divisi' : divisi
    }
    db.collection('events').document(emailEvent).set(data)

def event_delete(emailEvent) :
    db.collection('events').document(emailEvent).delete()