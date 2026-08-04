"""
Tests for the applications summary endpoint.
"""

from clients.api_client import APIClient
from helpers.auth_helper import login_user

def test_verify_authenticated_user_can_get_applications_summary():
    """
    Verify an authenticated user can retrieve application counts by status.
    """

    # make the call with the token in header
    applications_summary_endpoint = f"/api/v1/applications/summary"
    api_client = APIClient()
    response_body = api_client.get_json(applications_summary_endpoint,)

    assert response_body, "Expected a response but got empty or null. Endpoint: /api/v1/applications/summary"

    assert isinstance(response_body['potential'], int), f"Expected integer in the response body 'potential' field. But got {response_body['potential']}"
    assert isinstance(response_body['applied'], int), f"Expected integer in the response body 'applied' field. But got {response_body['applied']}"
    assert isinstance(response_body['in_progress'], int), f"Expected integer in the response body 'in_progress' field. But got {response_body['in_progress']}"
    assert isinstance(response_body['final_stage'], int), f"Expected integer in the response body 'final_stage' field. But got {response_body['final_stage']}"
    assert isinstance(response_body['hired'], int), f"Expected integer in the response body 'hired' field. But got {response_body['hired']}"
    assert isinstance(response_body['rejected'], int), f"Expected integer in the response body 'rejected' field. But got {response_body['rejected']}"
    assert isinstance(response_body['withdrawn'], int), f"Expected integer in the response body 'withdrawn' field. But got {response_body['withdrawn']}"
    assert isinstance(response_body['total'], int), f"Expected integer in the response body 'total' field. But got {response_body['total']}"