from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.misc import auth as fauth

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'spt-bemui-2add1.appspot.com'
    })

database = firestore.client()
bucket = storage.bucket()


def login(email, password):
    user = fauth.signIn(email, password)

    if 'error' in user:
        error = user['error']
        if error['code'] == 400:
            if error['message'] == 'INVALID_PASSWORD':
                return JsonResponse({'code': error['code'], 'message': 'Wrong password. Please try again.'})
            elif error['message'] == 'EMAIL_NOT_FOUND':
                return JsonResponse({'code': error['code'], 'message': 'Email not found. Please check your email.'})
            # Add more error conditions and corresponding custom error messages as needed
        elif error['code'] == 500:
            return JsonResponse({'code': error['code'], 'message': 'Internal server error. Please try again later.'})
        return

    return JsonResponse({'code': 200, 'user': user})


def uploadPhoto(file, destination_path):
    content_type = file.content_type
    file = file.file

    blob = bucket.blob(destination_path)
    metadata = {
        "firebaseStorageDownloadTokens": destination_path,
    }

    blob.content_type = content_type
    blob.metadata = metadata

    try:
        blob.upload_from_file(file)
        blob.make_public()

        return JsonResponse({
            'code': 200,
            'photoUrl': blob.public_url
        })
    except:

        return JsonResponse({
            'code': 500,
            'message': "There's something wrong. Please try again later."
        })


def getAccountInfo(sessionId):
    accountInfo = fauth.getAccountInfo(sessionId)

    if 'error' in accountInfo:
        error = accountInfo['error']
        if error['code'] == 400:
            if error['message'] == 'MISSING_ID_TOKEN':
                return JsonResponse({'code': error['code'], 'message': 'Session ID Missing. Please login first.'})
            elif error['message'] == 'INVALID_ID_TOKEN':
                return JsonResponse({'code': error['code'], 'message': 'Your session has expired. Please login again.'})
        elif error['code'] == 500:
            return JsonResponse({'code': error['code'], 'message': 'Internal server error. Please try again later.'})
        return

    return JsonResponse({'code': 200, 'accountInfo': accountInfo})
