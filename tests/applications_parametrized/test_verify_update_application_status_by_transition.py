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
    pytest.param("potential", "applied", id="potential_to_applied", marks=pytest.mark.tcid("029")),
    pytest.param("potential", "in_progress", id="potential_to_in_progress", marks=pytest.mark.tcid("030")),
    pytest.param("potential", "final_stage", id="potential_to_final_stage", marks=pytest.mark.tcid("031")),
    pytest.param("potential", "hired", id="potential_to_hired", marks=pytest.mark.tcid("032")),
    pytest.param("potential", "rejected", id="potential_to_rejected", marks=pytest.mark.tcid("033")),
    pytest.param("potential", "withdrawn", id="potential_to_withdrawn", marks=pytest.mark.tcid("034")),
    pytest.param("applied", "potential", id="applied_to_potential", marks=pytest.mark.tcid("035")),
    pytest.param("applied", "in_progress", id="applied_to_in_progress", marks=pytest.mark.tcid("036")),
    pytest.param("applied", "final_stage", id="applied_to_final_stage", marks=pytest.mark.tcid("037")),
    pytest.param("applied", "hired", id="applied_to_hired", marks=pytest.mark.tcid("038")),
    pytest.param("applied", "rejected", id="applied_to_rejected", marks=pytest.mark.tcid("039")),
    pytest.param("applied", "withdrawn", id="applied_to_withdrawn", marks=pytest.mark.tcid("040")),
    pytest.param("in_progress", "potential", id="in_progress_to_potential", marks=pytest.mark.tcid("041")),
    pytest.param("in_progress", "applied", id="in_progress_to_applied", marks=pytest.mark.tcid("042")),
    pytest.param("in_progress", "final_stage", id="in_progress_to_final_stage", marks=pytest.mark.tcid("043")),
    pytest.param("in_progress", "hired", id="in_progress_to_hired", marks=pytest.mark.tcid("044")),
    pytest.param("in_progress", "rejected", id="in_progress_to_rejected", marks=pytest.mark.tcid("045")),
    pytest.param("in_progress", "withdrawn", id="in_progress_to_withdrawn", marks=pytest.mark.tcid("046")),
    pytest.param("final_stage", "potential", id="final_stage_to_potential", marks=pytest.mark.tcid("047")),
    pytest.param("final_stage", "applied", id="final_stage_to_applied", marks=pytest.mark.tcid("048")),
    pytest.param("final_stage", "in_progress", id="final_stage_to_in_progress", marks=pytest.mark.tcid("049")),
    pytest.param("final_stage", "hired", id="final_stage_to_hired", marks=pytest.mark.tcid("050")),
    pytest.param("final_stage", "rejected", id="final_stage_to_rejected", marks=pytest.mark.tcid("051")),
    pytest.param("final_stage", "withdrawn", id="final_stage_to_withdrawn", marks=pytest.mark.tcid("052")),
    pytest.param("hired", "potential", id="hired_to_potential", marks=pytest.mark.tcid("053")),
    pytest.param("hired", "applied", id="hired_to_applied", marks=pytest.mark.tcid("054")),
    pytest.param("hired", "in_progress", id="hired_to_in_progress", marks=pytest.mark.tcid("055")),
    pytest.param("hired", "final_stage", id="hired_to_final_stage", marks=pytest.mark.tcid("056")),
    pytest.param("hired", "rejected", id="hired_to_rejected", marks=pytest.mark.tcid("057")),
    pytest.param("hired", "withdrawn", id="hired_to_withdrawn", marks=pytest.mark.tcid("058")),
    pytest.param("rejected", "potential", id="rejected_to_potential", marks=pytest.mark.tcid("059")),
    pytest.param("rejected", "applied", id="rejected_to_applied", marks=pytest.mark.tcid("060")),
    pytest.param("rejected", "in_progress", id="rejected_to_in_progress", marks=pytest.mark.tcid("061")),
    pytest.param("rejected", "final_stage", id="rejected_to_final_stage", marks=pytest.mark.tcid("062")),
    pytest.param("rejected", "hired", id="rejected_to_hired", marks=pytest.mark.tcid("063")),
    pytest.param("rejected", "withdrawn", id="rejected_to_withdrawn", marks=pytest.mark.tcid("064")),
    pytest.param("withdrawn", "potential", id="withdrawn_to_potential", marks=pytest.mark.tcid("065")),
    pytest.param("withdrawn", "applied", id="withdrawn_to_applied", marks=pytest.mark.tcid("066")),
    pytest.param("withdrawn", "in_progress", id="withdrawn_to_in_progress", marks=pytest.mark.tcid("067")),
    pytest.param("withdrawn", "final_stage", id="withdrawn_to_final_stage", marks=pytest.mark.tcid("068")),
    pytest.param("withdrawn", "hired", id="withdrawn_to_hired", marks=pytest.mark.tcid("069")),
    pytest.param("withdrawn", "rejected", id="withdrawn_to_rejected", marks=pytest.mark.tcid("070")),
]


@pytest.mark.parametrize(
    "initial_status, expected_status",
    STATUS_TRANSITIONS,
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
