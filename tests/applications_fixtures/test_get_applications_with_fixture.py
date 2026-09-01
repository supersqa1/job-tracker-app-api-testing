"""Fixture demo tests for authenticated API client setup.

These tests intentionally demonstrate how pytest fixtures provide reusable
authenticated clients while still being tracked as standalone automated test
cases.
"""

import pytest


@pytest.mark.tcid("081")
def test_verify_authenticated_user_can_get_paginated_applications(api_client):
    """Verify the authenticated API client fixture can retrieve applications."""

    # make the call
    response_body = api_client.get_json("/api/v1/applications")

    # verify
    assert response_body, "Response is empty."
