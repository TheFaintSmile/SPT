import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def user_peserta_create(idPeserta, email, password, nama, fakultas, jurusan, npm, pas_foto) :
    try:
        user = auth.create_user(
            uid=idPeserta, email=email, email_verified=False, password=password)
        print('Sucessfully created new user: {0}'.format(user.uid))
    except auth.EmailAlreadyExistsError:
        message = 'The user with the provided email already exists'
        return message;
    except auth.UidAlreadyExistsError:
        message = 'The user with the provided username already exists'
        return message;
    data = {
        'id': idPeserta,
        'email': email,
        'nama': nama,
        'fakultas' : fakultas,
        'jurusan' : jurusan,
        'npm' : npm,
        'pas_foto' : pas_foto
    }
    db.collection('user_peserta').document(idPeserta).set(data)
    return "";

def user_peserta_read(idPeserta):
    data = db.collection('user_peserta').document(idPeserta).get()
    print('Successfully fetched user data: {0}'.format(data))
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

def user_peserta_update_data(idPeserta, email, nama, fakultas, jurusan, npm, pas_foto):
    data = {
        'id': idPeserta,
        'email': email,
        'nama': nama,
        'fakultas' : fakultas,
        'jurusan' : jurusan,
        'npm' : npm,
        'pas_foto' : pas_foto
    }
    db.collection('user_peserta').document(idPeserta).set(data)
    return data

def user_peserta_delete(idPeserta):
    auth.delete_user(idPeserta)
    print('Successfully deleted user')