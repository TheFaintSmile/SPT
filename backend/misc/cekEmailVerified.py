from . import firebase_init

def cekEmailVerified(request):
    user = firebase_init.get_account_info(request.session['uid'])['users'][0]
    return user['emailVerified']

# cek_email = firebase_init.get_account_info(request.session['uid'])['users'][0]['emailVerified']
# print(cek_email)
