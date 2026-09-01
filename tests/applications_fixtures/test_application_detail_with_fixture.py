"""Fixture demo tests for using multiple fixtures in one test.

These tests intentionally demonstrate combining an authenticated API client
fixture with an application fixture while still being tracked as standalone
automated test cases.
"""

import pytest


@pytest.mark.tcid("082")
def test_verify_created_application_can_be_retrieved(application_fixture, api_client):
    """Verify an application created by a fixture can be retrieved by id."""
    # verify get app by id works, by creating app then making a get call

    # save the id
    application_id = application_fixture["id"]

    # do a get with the id
    response = api_client.get_json(f"/api/v1/applications/{application_id}")

    # verify
    assert response
    assert response["id"] == application_id
