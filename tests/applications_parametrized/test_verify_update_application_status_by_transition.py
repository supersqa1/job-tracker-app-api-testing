import pytest

from clients.api_client import APIClient
from helpers.application_helper import build_create_application_payload
from helpers.application_helper import create_application
from helpers.application_helper import delete_application
from helpers.application_helper import get_application


ALLOWED_STATUS = [
    "potential",
    "applied",
    "in_progress",
    "final_stage",
    "hired",
    "rejected",
    "withdrawn"
    ]

STATUS_TRANSITIONS = [
    (initial_status, expected_status)
    for initial_status in ALLOWED_STATUS
    for expected_status in ALLOWED_STATUS
    if initial_status != expected_status
    ]


@pytest.mark.parametrize(
    "initial_status, expected_status",
    STATUS_TRANSITIONS,
    ids=[f"{initial_status}_to_{expected_status}"
         for initial_status, expected_status in STATUS_TRANSITIONS]
    )
def test_verify_user_can_update_application_status(initial_status, expected_status):
    # import time; time.sleep(.5)
    print(f"Running status transition test: {initial_status} -> {expected_status}")

    # create api client
    api_client = APIClient()

    # create a new application with the initial status
    payload = build_create_application_payload(status=initial_status)
    application = create_application(api_client, payload=payload)
    application_id = application["id"]

    try:
        # update the application status
        update_endpoint = f"/api/v1/applications/{application_id}"
        update_payload = {
            "status": expected_status
            }
        update_response = api_client.patch_json(update_endpoint, data=update_payload)

        # verify the response contains the updated status
        assert update_response["status"] == expected_status, \
            f"Expected status '{expected_status}' but got '{update_response['status']}'"

        # fetch the application and verify the update is saved
        get_application_info = get_application(api_client, application_id)
        assert get_application_info["status"] == expected_status, \
            f"Saved status is '{get_application_info['status']}' instead of '{expected_status}'"
    finally:
        # clean up / teardown - delete the application created for the test
        delete_application(api_client, application_id)
