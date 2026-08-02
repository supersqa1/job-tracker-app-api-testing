import requests
from configs.settings import BASE_URL

def test_verify_public_status_endpoint():
    """
    Example response body:
        {
    "app_name": "SuperSQA Job Tracker",
    "api_version": "v1",
    "environment": "local",
    "server_time": "2026-08-02T01:55:28.264940Z"
    }
    """
    # make the call
    url = f"{BASE_URL}/api/v1/public/status"
    response = requests.get(url)

    # vererify the status code
    status_code = response.status_code
    assert status_code == 200, f"API /api/v1/public/status is not returning a 200 status code. Actual status code: {status_code}"

    # verify the body
    response_body = response.json()
    assert response_body["app_name"] == "SuperSQA Job Tracker"
    assert response_body["api_version"] == "v1"
    assert response_body["environment"] == "local", f"The environment expected in the api resposne but the value is {response_body['environment']}"
    assert response_body["server_time"], "The date time expected in the api resposne but the value is empty or null"
