import pytest

from helpers.application_helper import build_create_application_payload
from helpers.application_helper import create_application
from helpers.application_helper import get_application
from helpers.error_helper import verify_error_respsone

from clients.api_client import APIClient




@pytest.mark.tcid("013")
def test_verify_create_application_required_company_name():
    api_client = APIClient()

    # prepare a payload without company_name
    payload = build_create_application_payload()
    payload.pop("company_name")

    # make the call expecting an error
    response_json = create_application(api_client, payload, expected_status_code=422)

    # verify the error response
    verify_error_respsone(response_json, 'VALIDATION_ERROR', 'Request validation failed')
    # the lines below (the validation) are replaced by the method above. Keeping these lines for historical and educational reason
    # assert response_json["error"], f"Create application expecteing failure response did not have error. Actual: {response_json}"
    # assert response_json["error"]["code"] == 'VALIDATION_ERROR'
    # assert response_json["error"]["message"] == 'Request validation failed'
    # assert isinstance(response_json["error"]["details"], list), f"Error response expected to have a list in 'details' but it did not. Actual: {response_json}"

    # verify exactly the error is for the missing field
    assert response_json["error"]["details"][0]["loc"][1] == "company_name"

@pytest.mark.tcid("014")
def test_verify_create_application_rejects_invalid_status():
    api_client = APIClient()

    # create a payload with invalid status
    payload = build_create_application_payload(status="abcdefg")

    # make the call expecting error
    response_json = create_application(api_client, payload, expected_status_code=422)

    # verify the error response
    verify_error_respsone(response_json, 'VALIDATION_ERROR', 'Request validation failed')
    # the lines below (the validation) are replaced by the method above. Keeping these lines for historical and educational reason
    
    # assert response_json["error"], f"Create application expecteing failure response did not have error. Actual: {response_json}"
    # assert response_json["error"]["code"] == 'VALIDATION_ERROR'
    # assert response_json["error"]["message"] == 'Request validation failed'
    # assert isinstance(response_json["error"]["details"], list), f"Error response expected to have a list in 'details' but it did not. Actual: {response_json}"
    
    # verify exactly the error is for the missing field
    assert response_json["error"]["details"][0]["loc"][1] == "status"

@pytest.mark.tcid("015")
def test_verify_nonexistent_application_returns_not_found():
    api_client = APIClient()

    # make a get call with nonexistent id expecting a 404
    nonexistent_id = 999999
    response_json = get_application(api_client, nonexistent_id, expected_status_code=404)

    # verify the error response
    verify_error_respsone(response_json, 'NOT_FOUND', 'Application not found')
    # the lines below (the validation) are replaced by the method above. Keeping these lines for historical and educational reason
    # assert response_json["error"], f"Create application expecteing failure response did not have error. Actual: {response_json}"
    # assert response_json["error"]["code"] == 'NOT_FOUND'
    # assert response_json["error"]["message"] == 'Application not found'
    # assert isinstance(response_json["error"]["details"], list), f"Error response expected to have a list in 'details' but it did not. Actual: {response_json}"
    
    # verify exactly the error is for the missing field
    assert response_json["error"]["details"] == []

@pytest.mark.tcid("016")
def test_verifyapplications_list_requires_authentication():
    api_client = APIClient(authenticated=False)
    # make get call witout authenticating
    get_application_endpoint = "/api/v1/applications"
    get_response = api_client.get_json(get_application_endpoint, expected_status_code=401)

    # verfiy we get the correct error
    verify_error_respsone(get_response, 'AUTHENTICATION_REQUIRED', 'Authentication required')
