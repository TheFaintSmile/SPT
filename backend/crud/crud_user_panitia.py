import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def user_panitia_create(idPanitia, email, password, nama, fakultas, jurusan, npm, pas_foto, isPanitia) :
    idPanitia = idPanitia+"-"+email
    try:
        user = auth.create_user(
            uid=email, email=email, email_verified=False, password=password)
        print('Sucessfully created new user: {0}'.format(user.uid))
    except auth.EmailAlreadyExistsError:
        message = 'The user with the provided email already exists'
        return message;
    except auth.UidAlreadyExistsError:
        message = 'The user with the provided username already exists'
        return message;
    data = {
        'id': idPanitia,
        'email': email,
        'nama': nama,
        'fakultas' : fakultas,
        'jurusan' : jurusan,
        'npm' : npm,
        'pas_foto' : pas_foto,
        'isPanitia' : isPanitia
    }
    db.collection('user_panitia').document(idPanitia).set(data)
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

def user_panitia_update_data(idPanitia, email, nama, fakultas, jurusan, npm, pas_foto):
    data = {
        'id': idPanitia,
        'email': email,
        'nama': nama,
        'fakultas' : fakultas,
        'jurusan' : jurusan,
        'npm' : npm,
        'pas_foto' : pas_foto
    }
    db.collection('user_panitia').document(idPanitia).set(data)
    return data

def user_panitia_delete(idPanitia):
    auth.delete_user(idPanitia)
    print('Successfully deleted user')