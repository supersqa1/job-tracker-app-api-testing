"""Fixture demo tests for unauthenticated API client setup.

These tests intentionally demonstrate how pytest fixtures provide reusable API
clients while still being tracked as standalone automated test cases.
"""

import pytest


@pytest.mark.tcid("080")
def test_verify_applications_list_requires_authentication(unauthenticated_api_client):
    """Verify the unauthenticated API client fixture receives a 401 response."""

    # make the call
    response_json = unauthenticated_api_client.get_json(
        "/api/v1/applications",
        expected_status_code=401,
    )

    # verify
    assert response_json["error"]
    assert response_json["error"]["code"] == "AUTHENTICATION_REQUIRED"
    assert response_json["error"]["message"] == "Authentication required"
