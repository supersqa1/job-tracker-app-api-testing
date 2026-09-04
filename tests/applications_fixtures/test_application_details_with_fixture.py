"""Fixture demo tests for using multiple fixtures in one test.

These tests intentionally demonstrate combining an authenticated API client
fixture with a created application fixture while still being tracked as a
standalone automated test case.
"""

import pytest


@pytest.mark.tcid("082")
def test_verify_created_application_can_be_retrieved(created_application, api_client):
    """Verify an application created by a fixture can be retrieved by id."""
    application_id = created_application["id"]

    response = api_client.get_json(f"/api/v1/applications/{application_id}")

    assert response
    assert response["id"] == application_id
