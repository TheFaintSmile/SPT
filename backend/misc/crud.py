import firebase_admin
from firebase_admin import credentials, firestore, storage, auth, exceptions
from django.http import JsonResponse
import json

if not firebase_admin._apps:
    cred = credentials.Certificate("spt-bemui-privateKey.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'spt-bemui-2add1.appspot.com'
    })

database = firestore.client()
bucket = storage.bucket()


def findAndCreateUser(email, password, nama):
    try:
        # Check if email is already registered
        user = auth.get_user_by_email(email)

        message = 'The user with the provided email already exists'
        return JsonResponse({'code': 400, 'message': message})
    except exceptions.NotFoundError:
        try:
            # Iterate over all users and check if the display name matches
            for user in auth.list_users().iterate_all():
                if user.display_name == nama:
                    message = 'The user with the provided display name already exists'
                    return JsonResponse({'code': 400, 'message': message})

            # Create a new user
            user = auth.create_user(
                email=email, email_verified=False, password=password, display_name=nama
            )
            userId = user.uid

            return JsonResponse({'code': 200, 'userId': userId})
        except exceptions.FirebaseError:
            return JsonResponse({'code': 500, 'message': "There's something wrong. Please try again later."})


def changeEmail(uid, newEmail):
    try:
        # Update the user's email
        auth.update_user(uid, email=newEmail)

        return JsonResponse({'code': 200, 'message': 'Email updated successfully.'})
    except exceptions.FirebaseError:
        return JsonResponse({'code': 500, 'message': "There's something wrong. Please try again later."})


def verifyPassword(uid, currentPassword):
    try:
        auth.verify_password(uid, currentPassword)

        return JsonResponse({'code': 200, 'message': 'Password verified successfully.'})
    except exceptions.FirebaseError:
        return JsonResponse({'code': 500, 'message': "Kata Sandi Lama tidak sesuai."})


def changePassword(uid, newPassword, sessionId):
    try:
        auth.update_user(uid, password=newPassword)
        return JsonResponse({'code': 200, 'message': 'Password updated successfully.', 'sessionId': sessionId})
    except exceptions.FirebaseError:
        return JsonResponse({'code': 500, 'message': "There's something wrong. Please try again later."})


def putDataPeserta(data):
    # Insert data to peserta collection
    database.collection('peserta').document(data['idPeserta']).set(data)
    return JsonResponse({'code': 200, 'message': 'Successfully created new user'})


def putDataPanitia(data):
    # Insert data to panitia collection
    database.collection('panitia').document(data['idPanitia']).set(data)
    return JsonResponse({'code': 200, 'message': 'Successfully created new user'})


def getUserById(id):
    try:
        user = database.collection('panitia').document(id).get()
        if (user.exists):
            user = user.to_dict()
        else:
            user = database.collection(
                'peserta').document(id).get().to_dict()

        del user['password']

        return JsonResponse({'code': 200, 'message': 'Successfully get user', 'user': user})
    except exceptions.NotFoundError:
        return JsonResponse({'code': 404, 'message': 'User not found'})


def getAllPanitia():
    try:
        panitia = []
        for doc in database.collection('panitia').stream():
            p = doc.to_dict()
            del p['password']
            panitia.append(p)
        return JsonResponse({'code': 200, 'message': 'Successfully get all panitia', 'panitia': panitia})
    except exceptions.NotFoundError:
        return JsonResponse({'code': 404, 'message': 'Panitia not found'})


def getPesertaRelated(ids):
    try:
        allUsersRelated = []
        for divisi in ids:
            usersInEachDivisi = []
            for peserta in divisi:
                user = database.collection('peserta').document(
                    peserta['idPendaftar']).get()
                if (user.exists):
                    user = user.to_dict()

                dataPeserta = {
                    "idPendaftar": peserta['idPendaftar'],
                    "namaLengkap": user['namaPeserta'],
                    "fakultasPeserta": user['fakultasPeserta'],
                    "profilePicture": user['photoPeserta'],
                }

                usersInEachDivisi.append(dataPeserta)
            allUsersRelated.append(usersInEachDivisi)

        return JsonResponse({'code': 200, 'message': 'Successfully get users', 'users': allUsersRelated})
    except exceptions.NotFoundError:
        return JsonResponse({'code': 404, 'message': 'User not found'})


def getPanitiaRelated(ids):
    try:
        allUsersRelated = []
        for id in ids:
            idPanitia = id['idPanitia']
            idsDivisi = id['idsDivisi']

            user = database.collection('panitia').document(
                idPanitia).get()
            if (user.exists):
                user = user.to_dict()

            dataDivisi = []

            for divisiId in idsDivisi:
                for divisi in user['divisiAcara']:
                    if divisi['idDivisi'] == divisiId:
                        data = {
                            "idDivisi": divisi['idDivisi'],
                            "namaDivisi": divisi['namaDivisi'],
                        }

                        dataDivisi.append(data)
                        break

            dataPanitia = {
                "idPanitia": idPanitia,
                "namaPanitia": user['namaAcara'],
                "profilePicture": user['logoAcara'],
                "dataDivisi": dataDivisi,
            }

            allUsersRelated.append(dataPanitia)

        return JsonResponse({'code': 200, 'message': 'Successfully get users', 'users': allUsersRelated})
    except exceptions.NotFoundError:
        return JsonResponse({'code': 404, 'message': 'User not found'})


def joinIntoPanitia(idPeserta, idPanitia, dataPeserta, dataPanitia):
    try:
        # Get the document reference for peserta and panitia
        peserta_ref = database.collection('peserta').document(idPeserta)
        panitia_ref = database.collection('panitia').document(idPanitia)

        peserta_doc = peserta_ref.get()
        panitia_doc = panitia_ref.get()

        peserta_data = peserta_doc.to_dict()
        panitia_data = panitia_doc.to_dict()

        # Read the current value of panitiaYangDiikuti
        panitia_yang_diikuti = peserta_data.get('panitiaYangDiikuti', [])

        for panitia in panitia_yang_diikuti:
            if panitia['idPanitia'] == dataPeserta['idPanitia']:
                panitia['divisiYangDipilih'] = dataPeserta['divisiYangDipilih']
                panitia['kontakPendaftar'] = dataPeserta['kontakPendaftar']
                panitia['tugasUmum'] = dataPeserta['tugasUmum']
                panitia['tanggalDaftar'] = dataPeserta['tanggalDaftar']
                break
        else:
            panitia_yang_diikuti.append(dataPeserta)

        peserta_ref.update({'panitiaYangDiikuti': panitia_yang_diikuti})

        # Read the current value of pesertaYangMengikuti
        pesertaYangMengikuti = panitia_data.get('pesertaYangMengikuti', [])

        # Loop through the dataPanitia and update pesertaYangMengikuti
        for pendaftar in dataPanitia:
            idDivisi = pendaftar['idDivisi']
            peserta = pendaftar['detailPendaftar']['idPendaftar']

            # Find the corresponding divisi in pesertaYangMengikuti
            for divisi in pesertaYangMengikuti:
                if divisi['idDivisi'] == idDivisi:
                    # Check if pendaftar already exists in the divisi
                    for existing_pendaftar in divisi['peserta']:
                        if existing_pendaftar['detailPendaftar']['idPendaftar'] == peserta:
                            # Update the pendaftar data in pesertaYangMengikuti
                            existing_pendaftar['pilihanDivisi'] = pendaftar['pilihanDivisi']
                            existing_pendaftar['kontakPendaftar'] = pendaftar['kontakPendaftar']
                            existing_pendaftar['tugasUmum'] = pendaftar['tugasUmum']
                            existing_pendaftar['tugasKhusus'] = pendaftar['tugasKhusus']
                            existing_pendaftar['status'] = pendaftar['status']
                            break
                    else:
                        # If pendaftar doesn't exist in divisi, add as a new entry
                        divisi['peserta'].append({
                            'detailPendaftar': pendaftar['detailPendaftar'],
                            'pilihanDivisi': pendaftar['pilihanDivisi'],
                            'kontakPendaftar': pendaftar['kontakPendaftar'],
                            'tugasUmum': pendaftar['tugasUmum'],
                            'tugasKhusus': pendaftar['tugasKhusus'],
                            'status': pendaftar['status'],
                        })
                    break

        # Update the pesertaYangMengikuti field in Firestore with the updated data
        panitia_ref.update({'pesertaYangMengikuti': pesertaYangMengikuti})

        responseGet = getUserById(idPanitia)
        readResult = json.loads(responseGet.content)

        if readResult['code'] != 200:
            return responseGet

        return JsonResponse({'code': 200, 'message': 'Successfully joined panitia', 'user': readResult['user']})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': 'Error joining panitia'})


def updatePesertaStatus(idPeserta, idPanitia, idDivisi, newStatus):
    try:
        # Get the document reference for the panitia
        peserta_ref = database.collection('peserta').document(idPeserta)
        panitia_ref = database.collection('panitia').document(idPanitia)

        peserta_doc = peserta_ref.get()
        panitia_doc = panitia_ref.get()

        peserta_data = peserta_doc.to_dict()
        panitia_data = panitia_doc.to_dict()

        # Read the current value of pesertaYangMengikuti
        pesertaYangMengikuti = panitia_data.get('pesertaYangMengikuti', [])

        # Loop through pesertaYangMengikuti and find the corresponding peserta
        for divisi in pesertaYangMengikuti:
            if divisi['idDivisi'] == idDivisi:
                for pendaftar in divisi['peserta']:
                    if pendaftar['detailPendaftar']['idPendaftar'] == peserta_data['idPeserta']:
                        # Update the status of the peserta
                        pendaftar['status'] = newStatus
                        break
                else:
                    return JsonResponse({'code': 404, 'message': 'Peserta not found in the division.'})
                break
        else:
            return JsonResponse({'code': 404, 'message': 'Division not found.'})

        # Update the pesertaYangMengikuti field in Firestore with the updated data
        panitia_ref.update({'pesertaYangMengikuti': pesertaYangMengikuti})

        panitia_yang_diikuti = peserta_data.get('panitiaYangDiikuti', [])

        for panitia in panitia_yang_diikuti:
            if panitia['idPanitia'] == panitia_data['idPanitia']:
                for divisi in panitia['divisiYangDipilih']:
                    if divisi['idDivisi'] == idDivisi:
                        divisi['status'] = newStatus
                        break
                else:
                    return JsonResponse({'code': 404, 'message': 'Division not found.'})

        peserta_ref.update({'panitiaYangDiikuti': panitia_yang_diikuti})

        return JsonResponse({'code': 200, 'message': 'Peserta status updated successfully.'})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': 'Error updating peserta status.'})


def addingDivisi(idPanitia, data):
    try:
        panitia_ref = database.collection('panitia').document(idPanitia)

        panitia_doc = panitia_ref.get()

        panitia_data = panitia_doc.to_dict()

        divisiAcara = panitia_data.get('divisiAcara', [])

        # Check if the idDivisi already exists
        for divisi in divisiAcara:
            if divisi['idDivisi'] == data['idDivisi']:
                return JsonResponse({'code': 400, 'message': 'Divisi with the same id already exists.'})

        divisiAcara.append({
            'idDivisi': data['idDivisi'],
            'namaDivisi': data['namaDivisi'],
            'deskripsiDivisi': data['deskripsiDivisi'],
            'kuotaDivisi': data['kuotaDivisi'],
            'tugasUmumDivisi': data['tugasUmumDivisi'],
            'tugasKhususDivisi': data['tugasKhususDivisi'],
        })

        # Create a new entry in pesertaYangMengikuti for the new divisi
        pesertaYangMengikuti = panitia_data.get('pesertaYangMengikuti', [])
        pesertaYangMengikuti.append({
            'idDivisi': data['idDivisi'],
            'namaDivisi': data['namaDivisi'],
            'peserta': []
        })

        # Update the divisiAcara and pesertaYangMengikuti fields in Firestore
        panitia_ref.update({
            'divisiAcara': divisiAcara,
            'pesertaYangMengikuti': pesertaYangMengikuti
        })

        responseGet = getUserById(idPanitia)
        readResult = json.loads(responseGet.content)

        if readResult['code'] != 200:
            return responseGet

        return JsonResponse({'code': 200, 'message': f'Divisi {data["namaDivisi"]} added successfully.', 'user': readResult['user']})
    except Exception as e:

        return JsonResponse({'code': 500, 'message': 'Error adding divisi.'})


def updatingDivisi(idPanitia, data):
    try:
        panitia_ref = database.collection('panitia').document(idPanitia)

        panitia_doc = panitia_ref.get()

        panitia_data = panitia_doc.to_dict()

        divisiAcara = panitia_data.get('divisiAcara', [])

        # Find the corresponding divisi in divisiAcara
        for i, divisi in enumerate(divisiAcara):
            if divisi['idDivisi'] == data['idDivisi']:
                # Update the divisi details
                divisiAcara[i]['namaDivisi'] = data['namaDivisi']
                divisiAcara[i]['deskripsiDivisi'] = data['deskripsiDivisi']
                divisiAcara[i]['kuotaDivisi'] = int(data['kuotaDivisi'])
                divisiAcara[i]['tugasUmumDivisi'] = data['tugasUmumDivisi']
                divisiAcara[i]['tugasKhususDivisi'] = data['tugasKhususDivisi']
                break
        else:
            return JsonResponse({'code': 404, 'message': 'Divisi not found.'})

        # Update the divisi details in pesertaYangMengikuti
        pesertaYangMengikuti = panitia_data.get(
            'pesertaYangMengikuti', [])

        for peserta in pesertaYangMengikuti:
            if peserta['idDivisi'] == data['idDivisi']:
                peserta['namaDivisi'] = data['namaDivisi']
                break

        # Update the divisiAcara, pesertaYangMengikuti, and panitiaYangDiikuti fields in Firestore
        panitia_ref.update({
            'divisiAcara': divisiAcara,
            'pesertaYangMengikuti': pesertaYangMengikuti,
        })

        responseGet = getUserById(idPanitia)
        readResult = json.loads(responseGet.content)

        if readResult['code'] != 200:
            return responseGet

        return JsonResponse({'code': 200, 'message': f'Divisi {data["namaDivisi"]} updated successfully.', 'user': readResult['user']})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': 'Error updating divisi.'})


def deletingDivisi(idPanitia, idDivisi):
    try:
        panitia_ref = database.collection('panitia').document(idPanitia)

        panitia_doc = panitia_ref.get()

        panitia_data = panitia_doc.to_dict()

        divisiAcara = panitia_data.get('divisiAcara', [])

        # Find the corresponding divisi in divisiAcara
        namaDivisi = ''
        index_to_remove = -1
        for i, divisi in enumerate(divisiAcara):
            if divisi['idDivisi'] == idDivisi:
                namaDivisi = divisi['namaDivisi']
                index_to_remove = i
                break
        else:
            return JsonResponse({'code': 404, 'message': 'Divisi not found.'})

        # Remove the divisi from divisiAcara
        divisiAcara.pop(index_to_remove)

        # Remove the divisi from pesertaYangMengikuti
        pesertaYangMengikuti = panitia_data.get('pesertaYangMengikuti', [])
        pesertaYangMengikuti = [
            peserta for peserta in pesertaYangMengikuti if peserta['idDivisi'] != idDivisi]

        # Update the divisiAcara and pesertaYangMengikuti fields in Firestore
        panitia_ref.update({
            'divisiAcara': divisiAcara,
            'pesertaYangMengikuti': pesertaYangMengikuti,
        })

        responseGet = getUserById(idPanitia)
        readResult = json.loads(responseGet.content)

        if readResult['code'] != 200:
            return responseGet

        return JsonResponse({'code': 200, 'message': f'Divisi {namaDivisi} deleted successfully.', 'user': readResult['user']})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': 'Error deleting divisi.'})


def updateProfilePeserta(idPeserta, data):
    try:
        peserta_ref = database.collection('peserta').document(idPeserta)

        peserta_ref.update({'email': data['email'], 'namaPeserta': data['namaPeserta'],
                            'fakultasPeserta': data['fakultasPeserta'], 'jurusanPeserta': data['jurusanPeserta']})

        responseGet = getUserById(idPeserta)
        readResult = json.loads(responseGet.content)

        if readResult['code'] != 200:
            return responseGet

        return JsonResponse({'code': 200, 'message': 'Profile updated successfully.', 'user': readResult['user']})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': 'Error updating profile.'})


def updateProfilePanitia(idPanitia, data):
    try:
        panitia_ref = database.collection('panitia').document(idPanitia)
        panitia_ref.update({
            "email": data['email'],
            "namaAcara": data['namaAcara'],
            "deskripsiAcara": data['deskripsiAcara'],
            "tanggalMulaiAcara": data['tanggalMulaiAcara'],
            "tanggalSelesaiAcara": data['tanggalSelesaiAcara'],
            "bidangAcara": data['bidangAcara'],
            "kategoriAcara": data['kategoriAcara'],
            "tingkatAcara": data['tingkatAcara'],
            "timelineAcara": data['timelineAcara'],
        })

        responseGet = getUserById(idPanitia)
        readResult = json.loads(responseGet.content)

        if readResult['code'] != 200:
            return responseGet

        return JsonResponse({'code': 200, 'message': 'Profile updated successfully.', 'user': readResult['user']})

    except Exception as e:
        return JsonResponse({'code': 500, 'message': 'Error updating profile.'})
