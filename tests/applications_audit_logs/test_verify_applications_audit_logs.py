
from clients.api_client import APIClient
import sqlite3

def test_verify_create_application_writes_to_audit_logs():
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
    DATABASE_PATH = "/Users/admas/Desktop/QA-Automation/job-tracker-app-for-testing/backend/data/job_tracker.db"
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
