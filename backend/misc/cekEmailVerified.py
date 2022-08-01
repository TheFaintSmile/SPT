from . import firebase_init
from backend.crud import crud_user_peserta

def cekEmailVerified(request):
    user = firebase_init.get_account_info(request.session['uid'])['users'][0]
    return user['emailVerified']
