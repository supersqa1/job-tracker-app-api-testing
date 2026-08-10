
import pytest

from helpers.application_helper import create_application
from helpers.application_helper import get_application
from helpers.application_helper import delete_application
from helpers.application_helper import build_create_application_payload
from clients.api_client import APIClient

api_client = APIClient()

@pytest.mark.tcid("010")
def test_verify_user_can_update_application_notes():
    

    # Setup: create an application
    application_info = create_application(api_client)
    application_id = application_info["id"]
    notes_before = application_info["notes"]

    # make the update
    update_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {
        "notes": "API Automated Testing"
        }

    update_response = api_client.patch_json(update_endpoint, data=update_payload)
    # validate
    assert notes_before != update_response["notes"]
    assert update_payload["notes"] == update_response["notes"]

    # fetch the application and verify the udpate is saved
    get_application_info = get_application(api_client, application_id)
    assert get_application_info["notes"] == update_payload["notes"]

    # Teardown/cleaup - delete the application created for the test
    delete_application(api_client, application_id)

@pytest.mark.tcid("011")
def test_verify_user_can_update_application_remote_type():
    old_remote_type = "on_site"
    new_remote_type = "hybrid"
    # setup create application
    payload = build_create_application_payload(remote_type=old_remote_type)
    applicaiton_info = create_application(api_client, payload)
    application_id = applicaiton_info["id"]

    # update to remote_type = "hybrid"
    update_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {"remote_type": new_remote_type}

    update_response = api_client.patch_json(update_endpoint, data=update_payload)
    # validate
    assert update_response["remote_type"] != old_remote_type
    assert update_response["remote_type"] == new_remote_type

    # fetch the application and verify the udpate is saved
    get_application_info = get_application(api_client, application_id)
    assert get_application_info["remote_type"] == new_remote_type

    # Teardown/cleaup - delete the application created for the test
    delete_application(api_client, application_id)


@pytest.mark.tcid("012")
def test_verify_user_can_update_application_salary_range():
    old_salary_range = "$200k - $230k"
    new_salary_range = "$300k - $400k"
    # setup create application
    payload = build_create_application_payload(salary_range=old_salary_range)
    applicaiton_info = create_application(api_client, payload)
    application_id = applicaiton_info["id"]

    update_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {"salary_range": new_salary_range}

    update_response = api_client.patch_json(update_endpoint, data=update_payload)
    # validate
    assert update_response["salary_range"] != old_salary_range
    assert update_response["salary_range"] == new_salary_range

    # fetch the application and verify the udpate is saved
    get_application_info = get_application(api_client, application_id)
    assert get_application_info["salary_range"] == new_salary_range

    # Teardown/cleaup - delete the application created for the test
    delete_application(api_client, application_id)
