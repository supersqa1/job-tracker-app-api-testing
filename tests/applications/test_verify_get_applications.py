"""
Tests for the applications list endpoint.
"""

import pytest

from urllib3 import request
from configs.settings import BASE_URL
from clients.api_client import APIClient

from helpers.auth_helper import login_user

@pytest.mark.tcid("005")
def test_verify_authenticated_user_can_get_applications():
    """
    Verify an authenticated user can retrieve their applications list.
    """

    # make the api call with the token in the header
    get_applications_endpoint = f"/api/v1/applications"
    api_client = APIClient()
    response_body = api_client.get_json(get_applications_endpoint)

    # verify the api response body
    assert response_body, "Expected some data in response body but it was empty or None."
    assert isinstance(response_body, list), f"Expected the response body to be a list but got {type(response_body)}"
