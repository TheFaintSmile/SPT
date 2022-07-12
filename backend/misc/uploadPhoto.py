from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.misc import firebase_init

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
    'storageBucket' : 'spt-bemui-2add1.appspot.com'
    })

# fauth = firebase_init.firebaseInit().auth()
db = firestore.client()
ds = storage.bucket()

def uploadPhoto(request):
    print("test upload photo")
    if request.method == "POST" and request.FILES:
        file = request.FILES.get('file')
        content_type = file.content_type
        file = file.file
        id_firebase = request.POST.get("id_firebase")

        blob = ds.blob(id_firebase)
        metadata = {
            "firebaseStorageDownloadTokens": id_firebase,
        }
        blob.content_type = content_type
        blob.metadata = metadata
        blob.upload_from_file(file)

        return JsonResponse('sesai', safe=False)