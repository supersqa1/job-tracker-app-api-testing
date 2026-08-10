
import pytest

from clients.api_client import APIClient

@pytest.mark.tcid("007")
def test_verify_user_can_create_application():

    # create a payload
    payload = {
            "company_name": "SuperSQA",
            "job_url": "https://supersqa.com/jobs/us-test-engineer",
            "location": "Remote",
            "next_action": "Follow up with manager",
            "notes": "Submitted through api testing.",
            "remote_type": "remote",
            "role_title": "API Test Engineer",
            "salary_range": "$170k - $200k",
            "status": "applied"
            }

    # make the api call
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)

    # verify the response
    assert isinstance(create_application_json["id"], int), \
        f"Create application endpoint response ID is not integer. Actual: {create_application_json['id']}"
    assert create_application_json["company_name"] == payload["company_name"]
    assert create_application_json["job_url"] == payload["job_url"]
    assert create_application_json["location"] == payload["location"]
    assert create_application_json["next_action"] == payload["next_action"]
    assert create_application_json["notes"] == payload["notes"]
    assert create_application_json["remote_type"] == payload["remote_type"]
    assert create_application_json["role_title"] == payload["role_title"]
    assert create_application_json["salary_range"] == payload["salary_range"]
    assert create_application_json["status"] == payload["status"]
    assert create_application_json["description"] == None


    # do a get call and verify the item is actualy created
    application_id = create_application_json["id"]
    get_application_endpoint = f"/api/v1/applications/{application_id}"
    get_response = api_client.get_json(get_application_endpoint)

    assert create_application_json["id"] == get_response["id"]
    assert get_response["company_name"] == payload["company_name"]
    assert get_response["job_url"] == payload["job_url"]
    assert get_response["location"] == payload["location"]
    assert get_response["next_action"] == payload["next_action"]
    assert get_response["notes"] == payload["notes"]
    assert get_response["remote_type"] == payload["remote_type"]
    assert get_response["role_title"] == payload["role_title"]
    assert get_response["salary_range"] == payload["salary_range"]
    assert get_response["status"] == payload["status"]
    assert get_response["description"] == None

    # clean up / teardown - Delete the applicaiton we created
    delete_endpoint = f"/api/v1/applications/{application_id}"
    # we just make the call, the client verifies 204 response and that is good enough
    api_client.delete(delete_endpoint) 


     
