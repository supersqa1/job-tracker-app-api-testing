
from clients.api_client import APIClient
from helpers.application_helper import build_create_application_payload
from helpers.application_helper import create_application
import pytest

ALLOWED_STATUS = [
    "potential",
    "applied",
    "in_progress",
    "final_stage",
    "hired",
    "rejected",
    "withdrawn"
    ]

@pytest.mark.parametrize("expected_status", ALLOWED_STATUS)
def test_verify_user_can_create_application_with_status(expected_status):
    print(f"Running test for status: {expected_status}")

    # create api client
    api_client = APIClient()

    # build payload with desired status
    payload = build_create_application_payload(status=expected_status)

    # make the call
    response = create_application(api_client, payload=payload)

    # verify it was created correctly
    assert response['id'], f"Create application with status '{expected_status}' returned None for ID"
    assert response['status'] == expected_status, f"Create application with status '{expected_status}' returned {response['status']} for status"
