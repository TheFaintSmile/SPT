import pyrebase

def firebaseInit():
    # For Firebase JS SDK v7.20.0 and later, measurementId is optional
    config = {
        "apiKey": "AIzaSyAUesTUGLGrIwyEQSHFAG-rNKt5DSUGE8o",
        "authDomain": "spt-bemui-2add1.firebaseapp.com",
        "projectId": "spt-bemui-2add1",
        "storageBucket": "spt-bemui-2add1.appspot.com",
        "messagingSenderId": "826235535572",
        "appId": "1:826235535572:web:d8bdeda2059d2a3074fb41",
        "measurementId": "G-GWLCVVZCRL",
        "databaseURL": ""
    }
    
    return pyrebase.initialize_app(config)