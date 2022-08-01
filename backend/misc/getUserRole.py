from backend.crud.crud_user_panitia import user_panitia_read
from . import firebase_init
from backend.crud import crud_user_peserta

def getUserRole(request):
    user = firebase_init.get_account_info(request.session['uid'])['users'][0]
    user_role = crud_user_peserta.user_peserta_read(user['localId'])['isPanitia']
    return user_role
