from configs.settings import BASE_URL
import requests


def test_verify_user_can_login_with_valid_credentials():
    """
    Example response body:
    {
        "access_token": "string",
        "token_type": "bearer",
        "expires_in": 0,
        "user": {
            "id": 0,
            "email": "user@example.com",
            "full_name": "string",
            "role": "user",
            "is_active": true,
            "created_at": "2026-08-02T21:05:31.936Z",
            "updated_at": "2026-08-02T21:05:31.936Z"
        }
        }
    """

    # Make the call
    url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "email": "student@example.com",
        "password": "Password123!"
        }
    response = requests.post(url, json=payload)

    # Verify the response code
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # verify response body
    response_body = response.json()
    assert response_body["access_token"], f"Access token is required, but got {response_body['access_token']}"
    assert response_body["token_type"] == "bearer", "Token type is required"
    assert response_body["expires_in"], f"Expires in is required, but got {response_body['expires_in']}"
    assert response_body["user"], f"User is required, but got {response_body['user']}"
    assert response_body["user"]["id"], f"User id is required, but got {response_body['user']['id']}"
    assert response_body["user"]["email"] == payload["email"], f"User email is required, but got {response_body['user']['email']}"
    assert response_body["user"]["full_name"], f"User full name is required, but got {response_body['user']['full_name']}"
    assert response_body["user"]["role"], f"User role is required, but got {response_body['user']['role']}"
    assert response_body["user"]["is_active"], f"User is active is required, but got {response_body['user']['is_active']}"
    assert response_body["user"]["created_at"], f"User created at is required, but got {response_body['user']['created_at']}"
    assert response_body["user"]["updated_at"], f"User updated at is required, but got {response_body['user']['updated_at']}"


def test_verify_user_cannot_login_with_invalid_credentials():
    """
    Example response body:
    {
        "error": {
            "code": "INVALID_CREDENTIALS",
            "message": "Invalid email or password",
            "details": []
        }
        }
    """

        # Make the call
    url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "email": "student@example.com",
        "password": "Password1234"
        }
    response = requests.post(url, json=payload)

    # Verify the response code
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

    # verify the response body
    response_body = response.json()
    assert isinstance(response_body["error"], dict), "Expected response body to have 'error' dictionary."
    
    assert response_body["error"]["code"] == "INVALID_CREDENTIALS", \
        f"Expected response error.code to be 'INVALID_CREDENTIALS' but got '{response_body["error"]["code"]}'"

    assert response_body["error"]["message"] == "Invalid email or password", \
        f"Expected response error.message to be 'Invalid email or password' \
            but got '{response_body["error"]["message"]}'"

    assert response_body["error"]["details"] == [], \
        f"Expected response error.details to be '[]' but got '{response_body["error"]["details"]}'"