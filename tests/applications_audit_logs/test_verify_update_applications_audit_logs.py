"""
Tests that application updates write expected rows to audit logs.
"""

import pytest

from clients.api_client import APIClient
from clients.sql_client import SQLClient


@pytest.mark.tcid("019")
def test_verify_update_application_writes_to_audit_logs():
    """
    Verify updating an application records an ``updated`` audit log with status transition.
    """
    status_before = "potential"
    status_after = "applied"
    # make 'applications' call -> create application
    payload = {
            "company_name": "SuperSQA",
            "job_url": "https://supersqa.com/jobs/us-test-engineer",
            "location": "Remote",
            "next_action": "Follow up with manager",
            "notes": "Submitted through api testing.",
            "remote_type": "remote",
            "role_title": "API Test Engineer",
            "salary_range": "$170k - $200k",
            "status": status_before
            }

    # make the api call to create (test setup)
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)
    application_id = create_application_json["id"]

    # make api call to update
    update_endpoint = f"/api/v1/applications/{application_id}"
    update_data = {
        "status": status_after
        }
    api_client.patch(update_endpoint, update_data)

    # verify the log table using SQL
    # create connection
    sql = f"""SELECT * 
                FROM application_audit_logs
                WHERE application_id = {application_id}
                ORDER BY id DESC
                LIMIT 1;"""
    sql_client = SQLClient()
    audit_log = sql_client.execute_query(sql)

    assert audit_log, f"Expected rows in audit log for application id: {application_id}"
    assert audit_log[0]["action"] == "updated"
    assert audit_log[0]["old_status"] == status_before
    assert audit_log[0]["new_status"] == status_after
