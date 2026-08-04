"""
Tests for the auth login endpoint.
"""

from clients.api_client import APIClient

api_client = APIClient()

def test_verify_user_can_login_with_valid_credentials():
    """
    Verify valid credentials return a bearer token and user profile.
    """

    # Make the call
    endpoint = f"/api/v1/auth/login"
    payload = {
        "email": "student@example.com",
        "password": "Password123!"
        }
    
    # the client will make the call and return the json body of the response
    response_body = api_client.post_json(endpoint, data=payload)

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
    Verify invalid credentials return 401 with an INVALID_CREDENTIALS error.
    """

    # Make the call
    endpoint = f"/api/v1/auth/login"
    payload = {
        "email": "student@example.com",
        "password": "Password1234"
        }

    response_body = api_client.post_json(endpoint, data=payload, expected_status_code=401)

    # verify the response body
    assert isinstance(response_body["error"], dict), "Expected response body to have 'error' dictionary."
    
    assert response_body["error"]["code"] == "INVALID_CREDENTIALS", \
        f"Expected response error.code to be 'INVALID_CREDENTIALS' but got '{response_body["error"]["code"]}'"

    assert response_body["error"]["message"] == "Invalid email or password", \
        f"Expected response error.message to be 'Invalid email or password' \
            but got '{response_body["error"]["message"]}'"

    assert response_body["error"]["details"] == [], \
        f"Expected response error.details to be '[]' but got '{response_body["error"]["details"]}'"