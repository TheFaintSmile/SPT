import requests

API_KEY = "AIzaSyAUesTUGLGrIwyEQSHFAG-rNKt5DSUGE8o"

def sign_in_with_email_and_password(email, password):
    url_signin = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key='+API_KEY
    params = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }

    x = requests.post(url_signin, json = params)
    print(x.json())
    return x.json()

def get_account_info(token):
    url_signin = 'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key='+API_KEY
    params = {
        'idToken': token,
    }

    x = requests.post(url_signin, json = params)
    return x.json()

def send_email_verification_link(id_token):
    rest_api_url = 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key='+API_KEY
    params = {
        'requestType': 'VERIFY_EMAIL',
        'idToken': id_token
    }

    x = requests.post(rest_api_url, json = params)
    return x.json()