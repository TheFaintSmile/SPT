import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def user_panitia_create(idPanitia, nama, email, password, kategori, jumlah_divisi) :
    idPanitia = idPanitia+"-"+email
    try:
        user = auth.create_user(
            uid=idPanitia, email=email, email_verified=False, password=password)
        print('Sucessfully created new user: {0}'.format(user.uid))
    except auth.EmailAlreadyExistsError:
        message = 'The user with the provided email already exists'
        return message;
    except auth.UidAlreadyExistsError:
        message = 'The user with the provided username already exists'
        return message;
    
    # save to collection user_panitia
    data = {
        'id': idPanitia,
        'nama': nama,
        'email': email,
        'kategori' : kategori,
        'jumlah_divisi' : jumlah_divisi,
        'isPanitia' : True
    }
    db.collection('user_panitia').document(idPanitia).set(data)

    # save to collection user_peserta
    data_peserta = {
        'id': idPanitia,
        'isPanitia' : True
    }
    db.collection('user_peserta').document(idPanitia).set(data_peserta)
    return "";

def user_panitia_read(idPanitia):
    data = db.collection('user_panitia').document(idPanitia).get()
    print('Successfully fetched user data: {0}'.format(data))
    return data

def user_panitia_update_email(idPanitia, email):
    user = auth.update_user(
        idPanitia,
        email=email)

    print('Sucessfully updated user: {0}'.format(user.uid))

def user_panitia_update_password(idPanitia, password):
    user = auth.update_user(
        idPanitia,
        password=password)

    print('Sucessfully updated user: {0}'.format(user.uid))

def user_panitia_update_data(idPanitia, nama, email, kategori, jumlah_divisi):
    data = {
        'id': idPanitia,
        'nama': nama,
        'email': email,
        'kategori' : kategori,
        'jumlah_divisi' : jumlah_divisi,
        'isPanitia' : True
    }
    db.collection('user_panitia').document(idPanitia).set(data)
    return data

def user_panitia_delete(idPanitia):
    auth.delete_user(idPanitia)
    print('Successfully deleted user')