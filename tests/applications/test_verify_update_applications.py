import pytest

from clients.api_client import APIClient

@pytest.mark.tcid("008")
def test_verify_user_can_update_application_status():
    # Setup
    # create a new application (this is our test data)
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
    application_id = create_application_json["id"]

    # Test
    # Update the application
    update_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {
        "status": "in_progress"
        }
    patch_json_response = api_client.patch_json(update_endpoint, data=update_payload)
    assert patch_json_response["status"] == update_payload["status"]

    get_endpoint = f"/api/v1/applications/{application_id}"
    get_application_response = api_client.get_json(get_endpoint)
    assert get_application_response["status"] == update_payload["status"]

    # clean up / teardown - Delete the applicaiton we created
    delete_endpoint = f"/api/v1/applications/{application_id}"
    # we just make the call, the client verifies 204 response and that is good enough
    api_client.delete(delete_endpoint) 
