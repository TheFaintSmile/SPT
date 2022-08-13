import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def user_panitia_create(nama, email, password, kategori, jumlah_divisi) :
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
    
    # save to collection user_panitia
    data = {
        'nama': nama,
        'email': email,
        'kategori' : kategori,
        'jumlah_divisi' : jumlah_divisi,
        'isPanitia' : True
    }
    db.collection('user_panitia').document(email).set(data)

    # save to collection user_peserta
    data_peserta = {
        'email': email,
        'isPanitia' : True
    }
    db.collection('user_peserta').document(email).set(data_peserta)
    return "";

def user_panitia_read(emailPanitia):
    data = db.collection('user_panitia').document(emailPanitia).get().to_dict()
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

def user_panitia_update_data(nama, email, kategori, jumlah_divisi, local_id, email_lama):
    # idPanitia = idPanitia+"-"+email
    try:
        user = auth.update_user(local_id, email=email, display_name=nama)

        # jika email berubah, maka set email_verified ke False
        if email_lama != email:
            user = auth.update_user(local_id, email_verified=False)    # verifikasi email lagi
            db.collection('user_panitia').document(email_lama).delete()
            db.collection('user_peserta').document(email_lama).delete()

        print('Sucessfully update user: {0}'.format(user.uid))
    except :
        return "there is error"
    
    data = {
        'nama': nama,
        'email': email,
        'kategori' : kategori,
        'jumlah_divisi' : jumlah_divisi,
        'isPanitia' : True
    }
    db.collection('user_panitia').document(email).set(data)

    # save to collection user_peserta
    data_peserta = {
        'email': email,
        'isPanitia' : True
    }
    db.collection('user_peserta').document(email).set(data_peserta)
    return ""

def user_panitia_delete(idPanitia):
    auth.delete_user(idPanitia)
    print('Successfully deleted user')