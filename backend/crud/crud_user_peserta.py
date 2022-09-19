import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def user_peserta_create(email, password, nama, fakultas, jurusan, npm, pas_foto) :
    try:
        user = auth.create_user(
            email=email, email_verified=False, password=password, display_name=nama)
        print('Sucessfully created new user: {0}'.format(user.uid))
        
    except auth.EmailAlreadyExistsError:
        message = 'The user with the provided email already exists'
        return message;
    except auth.UidAlreadyExistsError:
        message = 'The user with the provided username already exists'
        return message;
    except :
        return "there is error"
    data = {
        'email': email,
        'nama': nama,
        'fakultas' : fakultas,
        'jurusan' : jurusan,
        'npm' : npm,
        'pas_foto' : pas_foto,
        'isPanitia' : False
    }
    db.collection('user_peserta').document(email).set(data)
    return "";

def user_peserta_read(emailPeserta):
    data = db.collection('user_peserta').document(emailPeserta).get().to_dict()
    print(data)
    return data

def user_peserta_update_email(idPeserta, email):
    user = auth.update_user(
        idPeserta,
        email=email)

    print('Sucessfully updated user: {0}'.format(user.uid))

def user_peserta_update_password(idPeserta, password):
    user = auth.update_user(
        idPeserta,
        password=password)

    print('Sucessfully updated user: {0}'.format(user.uid))

def user_peserta_update_data(email, nama, fakultas, jurusan, npm, pas_foto, localId, email_lama):
    try:
        user = auth.update_user(localId, email=email, display_name=nama)

        # jika email berubah, maka set email_verified ke False
        if email_lama != email:
            user = auth.update_user(localId, email_verified=False)    # verifikasi email lagi
            db.collection('user_peserta').document(email_lama).delete()
        
        print('Sucessfully update user: {0}'.format(user.uid))
    except :
        return "there is error"
    
    data = {
        'email': email,
        'nama': nama,
        'fakultas' : fakultas,
        'jurusan' : jurusan,
        'npm' : npm,
        'pas_foto' : pas_foto,
        'isPanitia' : False
    }
    db.collection('user_peserta').document(email).set(data)
    return ""

def user_peserta_delete(idPeserta):
    auth.delete_user(idPeserta)
    print('Successfully deleted user')

def user_register_event(email, events) :
    data = {
        'events' : events
    }
    db.collection('user_peserta').document(email).set(data, merge=True)