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
