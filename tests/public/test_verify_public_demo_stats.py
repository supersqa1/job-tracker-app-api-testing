"""
Tests for the public demo stats endpoint.
"""
import pytest
import requests
from configs.settings import BASE_URL

@pytest.mark.tcid("002")
def test_verify_public_demo_stats():
    """
    Verify the public demo stats endpoint returns seeded application counts.
    """
    # make the call
    url = f"{BASE_URL}/api/v1/public/demo-stats"
    response = requests.get(url)

    # verify the status code
    status_code = response.status_code
    assert status_code == 200, f"The status code expected is 200 but the actual status code is {status_code}"

    # verify the body
    response_body = response.json()

    # verify the number of keys is correct.
    assert len(response_body.keys()) == 2, f"The number of keys expected is 2 but the actual number of keys is {len(response_body.keys())}"

    # verify the values are of the correct type.
    assert isinstance(response_body["total_seeded_applications"], int), f"The total_seeded_applications expected is an integer but the actual value is {response_body['total_seeded_applications']}"
    assert isinstance(response_body["status_counts"], dict), f"The status_counts expected is a dictionary but the actual value is {response_body['status_counts']}"

    # verify the status_counts keys are correct.
    status_counts = response_body["status_counts"]
    for k, v in status_counts.items():
        assert isinstance(v, int), f"The value expected is an integer but the actual value is {v}"