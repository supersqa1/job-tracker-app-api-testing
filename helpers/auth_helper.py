from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD
import requests

def login_user(email=DEFAULT_USER_EMAIL, passowrd=DEFAULT_USER_PASSWORD):
    # get JWT token. 
    # login with user and get the token from the response
    # Make the call
    url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "email": email,
        "password": passowrd
        }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    response_body = response.json()

    return response_body["access_token"]