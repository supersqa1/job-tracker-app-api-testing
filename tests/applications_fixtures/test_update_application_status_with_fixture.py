"""Fixture demo tests for fixture-backed application status updates.

These tests intentionally demonstrate combining fixtures with parametrization
while still being tracked as standalone automated test cases.
"""

import pytest


@pytest.mark.parametrize(
    "new_status",
    [
        pytest.param("in_progress", marks=pytest.mark.tcid("083")),
        pytest.param("final_stage", marks=pytest.mark.tcid("084")),
        pytest.param("hired", marks=pytest.mark.tcid("085")),
    ],
)
def test_verify_user_can_update_application_status_with_fixture(api_client, application_fixture, new_status):
    """Verify an application fixture can be updated to the requested status."""
    application_id = application_fixture["id"]
    payload = {"status": new_status}

    response_body = api_client.patch_json(
        f"/api/v1/applications/{application_id}",
        payload
    )

    assert response_body["id"] == application_id
    assert response_body["status"] == new_status
