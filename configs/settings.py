"""
Environment-driven configuration for the Job Tracker API test framework.
"""

import os

# BASE_URL -> the url that does not include the endpoint
# which will change per environment
# https://dev.jobtracking.com
# https://staging.jobtracking.com
# http://localhost:3050

BASE_URL = os.getenv("BASE_URL", "http://localhost:3050")
DEFAULT_USER_EMAIL = os.getenv("DEFAULT_USER_EMAIL", "student@example.com")
DEFAULT_USER_PASSWORD = os.getenv("DEFAULT_USER_PASSWORD", "Password123!")
DATABASE_PATH = os.getenv("DATABASE_PATH", "/Users/admas/Desktop/QA-Automation/job-tracker-app-for-testing/backend/data/job_tracker.db")