# Code Checkpoints

This repo uses Git tags as course checkpoints so students/instructor can return to important framework states.

## framework-04-base-url-config

Current checkpoint after the first public API tests and config refactor.

Includes:
- `requirements.txt` with `pytest` and `requests`
- `docs/test-cases-job-tracker-api.csv`
- `tests/test_verify_public_status_endpoint.py`
- `tests/test_verify_public_demo_stats.py`
- `configs/settings.py` with `BASE_URL`

Course state:
- First public status endpoint test implemented
- Public demo stats endpoint test implemented
- Base URL moved out of test files into shared settings
- Next course step: add login API tests

## framework-05-login-tests

Checkpoint after adding authentication login tests.

Includes:
- Positive login test with valid student credentials
- Negative login test with invalid credentials
- Auth tests organized under `tests/auth/`
- Public tests organized under `tests/public/`

Course state:
- Students have seen GET public API tests
- Students have seen POST login API tests
- Next course step: test protected API endpoint using auth token

## framework-06-auth-helper

Checkpoint after adding protected application tests and a reusable login helper.

Includes:
- `helpers/auth_helper.py` with `login_user()`
- default user credentials in `configs/settings.py`
- protected `GET /api/v1/applications` test
- protected `GET /api/v1/applications/summary` test

Course state:
- Students have seen Bearer token auth in protected API tests
- Repeated login/token code has been refactored into a helper
- Next course step: create a reusable API client
