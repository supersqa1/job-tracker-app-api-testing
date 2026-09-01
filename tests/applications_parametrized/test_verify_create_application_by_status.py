import pytest

from clients.api_client import APIClient
from helpers.application_helper import build_create_application_payload
from helpers.application_helper import create_application

ALLOWED_STATUS = [
    pytest.param("potential", marks=pytest.mark.tcid("022")),
    pytest.param("applied", marks=pytest.mark.tcid("023")),
    pytest.param("in_progress", marks=pytest.mark.tcid("024")),
    pytest.param("final_stage", marks=pytest.mark.tcid("025")),
    pytest.param("hired", marks=pytest.mark.tcid("026")),
    pytest.param("rejected", marks=pytest.mark.tcid("027")),
    pytest.param("withdrawn", marks=pytest.mark.tcid("028")),
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
    assert response["id"], f"Create application with status '{expected_status}' returned None for ID"
    assert response["status"] == expected_status, f"Create application with status '{expected_status}' returned {response['status']} for status"
