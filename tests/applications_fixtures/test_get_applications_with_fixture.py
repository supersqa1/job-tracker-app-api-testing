"""Fixture demo tests for authenticated API client setup.

These tests intentionally demonstrate how pytest fixtures provide reusable
authenticated clients while still being tracked as standalone automated test
cases.
"""

import pytest


@pytest.mark.tcid("081")
def test_verify_authenticated_user_can_get_paginated_applications(api_client):
    """Verify the authenticated API client fixture can retrieve paginated applications."""
    response_body = api_client.get_json(
        "/api/v1/applications?paginated=true&limit=2&offset=0"
    )

    assert "items" in response_body
    assert "total" in response_body
    assert response_body["limit"] == 2
    assert response_body["offset"] == 0
    assert isinstance(response_body["items"], list)


def test_verify_authenticated_user_can_limit_paginated_applications(api_client):
    """Verify the authenticated API client fixture supports pagination limits."""
    response_body = api_client.get_json(
        "/api/v1/applications?paginated=true&limit=1&offset=0"
    )

    assert response_body["limit"] == 1
    assert response_body["offset"] == 0
    assert len(response_body["items"]) <= 1
