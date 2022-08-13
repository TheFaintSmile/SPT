from . import firebase_init
from backend.crud import crud_user_peserta

def getJurusan(request):
    user = firebase_init.get_account_info(request.session['uid'])['users'][0]
    jurusan = crud_user_peserta.user_peserta_read(user['email'])['jurusan']
    return jurusan

def getFakultas(request):
    user = firebase_init.get_account_info(request.session['uid'])['users'][0]
    fakultas = crud_user_peserta.user_peserta_read(user['email'])['fakultas']
    return fakultas
