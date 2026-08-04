
from configs.settings import BASE_URL
import requests
from helpers.auth_helper import login_user

def test_verify_authenticated_user_can_get_applications_summary():

    # login and get the jwt token
    access_token= login_user()
 
    # make the call with the token in header
    get_applications_url = f"{BASE_URL}/api/v1/applications/summary"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(get_applications_url, headers=headers)

    # verify the status code
    assert response.status_code == 200, \
        f"Get applications/summary api response expected to be 200 but actual was {response.status_code} Endpoint: '/api/v1/applications/summary'"

    # verify the response body
    response_body = response.json()
    assert response_body, "Expected a response but got empty or null. Endpoint: /api/v1/applications/summary"

    assert isinstance(response_body['potential'], int), f"Expected integer in the response body 'potential' field. But got {response_body['potential']}"
    assert isinstance(response_body['applied'], int), f"Expected integer in the response body 'applied' field. But got {response_body['applied']}"
    assert isinstance(response_body['in_progress'], int), f"Expected integer in the response body 'in_progress' field. But got {response_body['in_progress']}"
    assert isinstance(response_body['final_stage'], int), f"Expected integer in the response body 'final_stage' field. But got {response_body['final_stage']}"
    assert isinstance(response_body['hired'], int), f"Expected integer in the response body 'hired' field. But got {response_body['hired']}"
    assert isinstance(response_body['rejected'], int), f"Expected integer in the response body 'rejected' field. But got {response_body['rejected']}"
    assert isinstance(response_body['withdrawn'], int), f"Expected integer in the response body 'withdrawn' field. But got {response_body['withdrawn']}"
    assert isinstance(response_body['total'], int), f"Expected integer in the response body 'total' field. But got {response_body['total']}"