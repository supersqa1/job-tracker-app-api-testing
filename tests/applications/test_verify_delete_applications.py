
import pytest

from clients.api_client import APIClient

@pytest.mark.tcid("009")
def test_verify_user_can_delete_application():
    # Setup - create an application
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
    # make the delete call
    delete_endpoint = f"/api/v1/applications/{application_id}"
    api_client.delete(delete_endpoint)

    # verify it is deleted
    # to verify it is deleted we should make a get call and expect 404
    # the 'get' method in api client automatically will check the status code
    # so if we got 404 that means the test pass
    get_endpoint = f"/api/v1/applications/{application_id}"
    api_client.get(get_endpoint, expected_status_code=404)

    # it would be nice if we use SQL go to database directly and 
    # verify that the item is deleted
