from backend.misc import utils
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from backend.misc.crud import findAndCreateUser, changeEmail, changePassword, putDataPeserta, putDataPanitia, getUserById, getAllPanitia, joinIntoPanitia, updatePesertaStatus, addingDivisi, updatingDivisi, deletingDivisi, updateProfilePeserta, updateProfilePanitia, getPesertaRelated, getPanitiaRelated
import json


@csrf_exempt
def login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    responseLogin = utils.login(email, password)

    loginStatus = json.loads(responseLogin.content)

    if (loginStatus['code'] != 200):
        return responseLogin

    user = loginStatus['user']

    response = JsonResponse(
        {'code': 200, 'message': 'You have successfully login.', 'sessionId': user['idToken']})
    response.set_cookie('sessionId', user['idToken'])
    return response


def logout(request):
    response = JsonResponse(
        {'code': 200, 'message': 'You have successfully logout.'})
    response.delete_cookie('sessionId')
    return response


@csrf_exempt
def registerPeserta(request):
    namaPeserta = request.POST.get("namaPeserta")
    email = request.POST.get("email")
    password = request.POST.get("password")
    photoPeserta = request.FILES.get("photoPeserta")

    if photoPeserta is None:
        return JsonResponse({'code': 400, 'message': 'No photo uploaded.'})

    responseInCreating = findAndCreateUser(email, password, namaPeserta)
    successCreating = json.loads(responseInCreating.content)

    if (successCreating['code'] != 200):
        return responseInCreating

    responseUploadPhoto = utils.uploadPhoto(
        photoPeserta, f"PESERTA/PHOTO/{uuid4()}")

    uploadedPhoto = json.loads(responseUploadPhoto.content)

    if (uploadedPhoto['code'] != 200):
        return (responseUploadPhoto)

    data = {
        "idPeserta": successCreating['userId'],
        "email": email,
        "namaPeserta": namaPeserta,
        'fakultasPeserta': request.POST.get('fakultasPeserta'),
        'jurusanPeserta': request.POST.get('jurusanPeserta'),
        'password': password,
        "photoPeserta": uploadedPhoto['photoUrl'],
        "panitiaYangDiikuti": [],
        'isPanitia': False
    }

    return putDataPeserta(data)


@csrf_exempt
def registerPanitia(request):
    namaAcara = request.POST.get('namaAcara')
    password = request.POST.get('password')
    email = request.POST.get('email')
    logoAcara = request.FILES.get("logoAcara")

    if logoAcara is None:
        return JsonResponse({'code': 400, 'message': 'No logo uploaded.'})

    responseInCreating = findAndCreateUser(email, password, namaAcara)
    successCreating = json.loads(responseInCreating.content)

    if (successCreating['code'] != 200):
        return responseInCreating

    responseUploadPhoto = utils.uploadPhoto(
        logoAcara, f"PANITIA/PHOTO/{uuid4()}")

    uploadedPhoto = json.loads(responseUploadPhoto.content)

    if (uploadedPhoto['code'] != 200):
        return (responseUploadPhoto)

    divisiAcara = json.loads(request.POST.get('divisiAcara'))

    pesertaYangMengikuti = []

    for divisi in divisiAcara:
        pesertaYangMengikutiDivisi = {
            'idDivisi': divisi['idDivisi'],
            'namaDivisi': divisi['namaDivisi'],
            'peserta': []
        }

        pesertaYangMengikuti.append(pesertaYangMengikutiDivisi)

    data = {
        "idPanitia": successCreating['userId'],
        "email": email,
        "password": password,
        "namaAcara": namaAcara,
        "deskripsiAcara": request.POST.get('deskripsiAcara'),
        "bidangAcara": request.POST.get('bidangAcara'),
        "kategoriAcara": request.POST.get('kategoriAcara'),
        "tanggalMulaiAcara": request.POST.get('tanggalMulaiAcara'),
        "tanggalSelesaiAcara": request.POST.get('tanggalSelesaiAcara'),
        "tingkatAcara": request.POST.get('tingkatAcara'),
        "timelineAcara": json.loads(request.POST.get('timelineAcara')),
        "divisiAcara": divisiAcara,
        "pesertaYangMengikuti": pesertaYangMengikuti,
        "logoAcara": uploadedPhoto['photoUrl'],
        "isPanitia": True,
    }

    return putDataPanitia(data)


def getArbitraryUser(request):
    sessionId = request.COOKIES.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    responseGet = getUserById(accountInfo['users'][0]['localId'])

    readResult = json.loads(responseGet.content)

    if readResult['code'] != 200:
        return responseGet

    return JsonResponse({
        'code': 200,
        'user': readResult['user']
    })


def getAllArbitraryPanitia(request):
    return getAllPanitia()


@csrf_exempt
def joinPanitia(request):
    sessionId = request.POST.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    idPanitia = request.POST.get('idPanitia')

    responseGet = getUserById(idPanitia)

    readResult = json.loads(responseGet.content)

    if readResult['code'] != 200:
        return responseGet

    panitia = readResult['user']

    # Get essential information
    tugasUmum = request.POST.get("tugasUmum")
    divisiYangDipilih = json.loads(request.POST.get('divisiYangDipilih'))
    kontakPendaftar = request.POST.get("kontakPendaftar")
    tanggalDaftar = request.POST.get("tanggalDaftar")

    dataPeserta = {
        "idPanitia": idPanitia,
        "namaPanitia": panitia['namaAcara'],
        "kontakPendaftar": kontakPendaftar,
        # [{"namaDivisi": "Divisi 1", "tugasKhusus": "Tugas Khusus 1"}, {"namaDivisi": "Divisi 2", "tugasKhusus": "Tugas Khusus 2"}}]
        "divisiYangDipilih": divisiYangDipilih,
        "tugasUmum": tugasUmum,
        "status": "pending",
        "tanggalDaftar": tanggalDaftar,
    }

    # Create a set of all 'namaDivisi' values from 'panitia['divisiAcara']'
    panitia_divisi_names = {divisi['namaDivisi']
                            for divisi in panitia['divisiAcara']}

    # Data to be stored in panitia collection
    dataPanitia = []

    detailPendaftar = json.loads(request.POST.get('detailPendaftar'))

    for selected_divisi in divisiYangDipilih:
        if selected_divisi['namaDivisi'] in panitia_divisi_names:
            dataPanitia.append({
                "idDivisi": selected_divisi['idDivisi'],
                "namaDivisi": selected_divisi['namaDivisi'],
                "pilihanDivisi": selected_divisi['pilihanDivisi'],
                "tugasUmum": tugasUmum,
                "tugasKhusus": selected_divisi['tugasKhusus'],
                "detailPendaftar": detailPendaftar,
                "kontakPendaftar": kontakPendaftar,
                "status": selected_divisi['status'],
            })
        else:
            return JsonResponse({'code': 400, 'message': 'Divisi yang dipilih tidak ada.'})

    return joinIntoPanitia(accountInfo['users'][0]['localId'], panitia['idPanitia'], dataPeserta, dataPanitia)


@csrf_exempt
def updateStatus(request):
    sessionId = request.POST.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    idPendaftar = request.POST.get('idPendaftar')

    responseGet = getUserById(idPendaftar)

    readResult = json.loads(responseGet.content)

    if readResult['code'] != 200:
        return responseGet

    peserta = readResult['user']

    idDivisi = request.POST.get('idDivisi')
    status = request.POST.get('status')

    return updatePesertaStatus(peserta['idPeserta'], accountInfo['users'][0]['localId'], idDivisi, status)


@csrf_exempt
def addDivisi(request):
    sessionId = request.POST.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    data = {
        "idDivisi": request.POST.get('idDivisi'),
        "namaDivisi": request.POST.get('namaDivisi'),
        "deskripsiDivisi": request.POST.get('deskripsiDivisi'),
        "kuotaDivisi": int(request.POST.get('kuotaDivisi')),
        "tugasUmumDivisi": request.POST.get('tugasUmumDivisi'),
        "tugasKhususDivisi": request.POST.get('tugasKhususDivisi'),
    }

    return addingDivisi(accountInfo['users'][0]['localId'], data)


@csrf_exempt
def updateDivisi(request):
    sessionId = request.POST.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    data = {
        "idDivisi": request.POST.get('idDivisi'),
        "namaDivisi": request.POST.get('namaDivisi'),
        "deskripsiDivisi": request.POST.get('deskripsiDivisi'),
        "kuotaDivisi": int(request.POST.get('kuotaDivisi')),
        "tugasUmumDivisi": request.POST.get('tugasUmumDivisi'),
        "tugasKhususDivisi": request.POST.get('tugasKhususDivisi'),
    }

    return updatingDivisi(accountInfo['users'][0]['localId'], data)


@csrf_exempt
def deleteDivisi(request):
    sessionId = request.POST.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    return deletingDivisi(accountInfo['users'][0]['localId'], request.POST.get('idDivisi'))


@csrf_exempt
def updateProfile(request):
    sessionId = request.POST.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    newEmail = request.POST.get('email')
    if (accountInfo['users'][0]['email'] != newEmail):
        responseChangeEmail = changeEmail(
            accountInfo['users'][0]['localId'], newEmail)
        successChangeEmail = json.loads(responseChangeEmail.content)

        if (successChangeEmail['code'] != 200):
            return responseChangeEmail

    if (request.POST.get('isPanitia') == 'true'):
        logoAcara = request.FILES.get("logoAcara")
        dataToBeUpdated = {
            "namaAcara": request.POST.get('namaAcara'),
            "deskripsiAcara": request.POST.get('deskripsiAcara'),
            "email": newEmail,
            "bidangAcara": request.POST.get('bidangAcara'),
            "kategoriAcara": request.POST.get('kategoriAcara'),
            "tanggalMulaiAcara": request.POST.get('tanggalMulaiAcara'),
            "tanggalSelesaiAcara": request.POST.get('tanggalSelesaiAcara'),
            "tingkatAcara": request.POST.get('tingkatAcara'),
            "timelineAcara": json.loads(request.POST.get('timelineAcara')),
        }

        if logoAcara is not None:
            responseUploadPhoto = utils.uploadPhoto(
                logoAcara, f"PANITIA/PHOTO/{uuid4()}")

            uploadedPhoto = json.loads(responseUploadPhoto.content)

            if (uploadedPhoto['code'] != 200):
                return (responseUploadPhoto)

            dataToBeUpdated['logoAcara'] = uploadedPhoto['photoUrl']

        return updateProfilePanitia(accountInfo['users'][0]['localId'], dataToBeUpdated)

    else:
        photoPeserta = request.FILES.get("photoPeserta")

        dataToBeUpdated = {
            "email": newEmail,
            "namaPeserta": request.POST.get('namaPeserta'),
            "fakultasPeserta": request.POST.get('fakultasPeserta'),
            "jurusanPeserta": request.POST.get('jurusanPeserta'),
        }

        if photoPeserta is not None:
            responseUploadPhoto = utils.uploadPhoto(
                photoPeserta, f"PESERTA/PHOTO/{uuid4()}")

            uploadedPhoto = json.loads(responseUploadPhoto.content)

            if (uploadedPhoto['code'] != 200):
                return (responseUploadPhoto)

            dataToBeUpdated['photoPeserta'] = uploadedPhoto['photoUrl']

        return updateProfilePeserta(accountInfo['users'][0]['localId'], dataToBeUpdated)


@csrf_exempt
def updatePassword(request):
    currentPassword = request.POST.get('currentPassword')
    newPassword = request.POST.get('newPassword')

    if (currentPassword == newPassword):
        return JsonResponse({'code': 400, 'message': 'Password baru tidak boleh sama dengan password lama.'})

    sessionId = request.POST.get('sessionId')

    responseAccountInfo = utils.getAccountInfo(sessionId)
    successRetrieving = json.loads(responseAccountInfo.content)

    if (successRetrieving['code'] != 200):
        return responseAccountInfo

    accountInfo = successRetrieving['accountInfo']

    responseLogin = utils.login(
        accountInfo['users'][0]['email'], currentPassword)

    loginStatus = json.loads(responseLogin.content)

    if (loginStatus['code'] != 200):
        return responseLogin

    user = loginStatus['user']

    return changePassword(accountInfo['users'][0]['localId'], newPassword, user['idToken'])


@csrf_exempt
def fetchUsersRelated(request):
    ids = json.loads(request.POST.get('ids'))
    mode = request.POST.get('mode')

    if (mode != 'panitia'):
        return getPanitiaRelated(ids)
    else:
        return getPesertaRelated(ids)
