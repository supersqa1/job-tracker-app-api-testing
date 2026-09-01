"""
Tests that application creation writes expected rows to audit logs.
"""

import sqlite3

import pytest

from clients.api_client import APIClient
from clients.sql_client import SQLClient
from configs.settings import DATABASE_PATH

@pytest.mark.tcid("017")
def test_verify_create_application_writes_to_audit_logs():
    """
    Verify creating an application records a ``created`` audit log via raw SQL.

    Kept intentionally alongside the V2 test below to compare direct sqlite3
    usage with the shared ``SQLClient`` helper.
    """
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
            "status": "potential"
            }

    # make the api call
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)
    application_id = create_application_json["id"]

    # verify the log table using SQL
    # create connection
    # TODO: use proper path
#     DATABASE_PATH = "/Users/admas/Desktop/QA-Automation/job-tracker-app-for-testing/backend/data/job_tracker.db"
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    sql = f"""SELECT * 
            FROM application_audit_logs
            WHERE application_id = {application_id};"""
    cursor.execute(sql)
    audit_log = cursor.fetchone()
    cursor.close()
    connection.close()

    assert audit_log, f"Expected rows in audit log for application id: {application_id}"
    assert audit_log["application_id"] == application_id
    assert audit_log["action"] == "created"
    assert audit_log["user_id"]


@pytest.mark.tcid("018")
def test_verify_create_application_writes_to_audit_logs_V2():
    """
    Verify creating an application records a ``created`` audit log via SQLClient.

    Same scenario as the V1 test above, using the shared database helper.
    """
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
            "status": "potential"
            }

    # make the api call
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)
    application_id = create_application_json["id"]

    # verify the log table using SQL
    # create connection
    # TODO: use proper path
    sql = f"""SELECT * 
            FROM application_audit_logs
            WHERE application_id = {application_id};"""
    sql_client = SQLClient()
    audit_log = sql_client.execute_query(sql)

    assert audit_log, f"Expected rows in audit log for application id: {application_id}"
    assert audit_log[0]["application_id"] == application_id
    assert audit_log[0]["action"] == "created"
    assert audit_log[0]["user_id"]
