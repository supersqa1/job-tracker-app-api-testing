+# SuperSQA Job Tracker API Test Automation

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white)
![API](https://img.shields.io/badge/Testing-REST%20API-6C47FF)
![Portfolio](https://img.shields.io/badge/Project-Portfolio-111827)

> A maintainable, data-driven API test framework built to explore real-world QA practices with Python, pytest, HTTP clients, authentication, database assertions, and actionable test reporting.

## Table of Contents

- [Overview](#overview)
- [Application Under Test](#application-under-test)
- [Why This Project Exists](#why-this-project-exists)
- [What Is Covered](#what-is-covered)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Tests](#running-the-tests)
- [Useful Commands](#useful-commands)
- [Example Test Flow](#example-test-flow)
- [Reports and Test Artifacts](#reports-and-test-artifacts)
- [Test Design](#test-design)
- [Learning Outcomes](#learning-outcomes)
- [Roadmap](#roadmap)
- [Related Projects](#related-projects)

## Overview

This repository contains automated API tests for the **SuperSQA Job Tracker**, a full-stack application for managing job applications, statuses, follow-ups, interviews, and notes.

The project is intentionally designed as a learning and practice environment for API testing. It demonstrates how a QA engineer can move beyond isolated requests and build a small but credible automation framework around a real application and its business workflows.

The suite currently includes **21 custom test cases**, plus parametrized scenarios that expand coverage across supported application statuses and status transitions.

## Application Under Test

The tests target the SuperSQA Job Tracker API. The application includes:

- FastAPI backend services
- SQLite persistence
- JWT-based authentication
- Protected and public API endpoints
- Job application CRUD workflows
- Application status tracking and summary statistics
- Audit logging
- API-key creation and storage
- OpenAPI/Swagger documentation

| Resource | Link |
|---|---|
| Application repository used for testing | [supersqa1/job-tracker-app-for-testing](https://github.com/supersqa1/job-tracker-app-for-testing) |
| Continuing portfolio application | [supersqa1/supersqa-job-tracker](https://github.com/supersqa1/supersqa-job-tracker) |
| This API automation repository | [supersqa1/job-tracker-app-api-testing](https://github.com/supersqa1/job-tracker-app-api-testing) |
| Local application URL | `http://localhost:3050` |
| Local Swagger UI | `http://localhost:3050/docs` |

The application is normally run locally. The test framework defaults to `http://localhost:3050`; a different environment can be supplied through `BASE_URL`.

## Why This Project Exists

This is a **portfolio project and a practical API-testing learning project**. It is intended to show the ability to:

- Understand an API from its OpenAPI contract and test-case documentation
- Organize tests by feature and risk
- Validate status codes, response bodies, data types, and business rules
- Test both successful and unsuccessful requests
- Reuse authentication and HTTP behavior through framework helpers
- Use parameterization for efficient data-driven coverage
- Verify side effects in the database when an API changes persisted data
- Produce HTML and JUnit reports suitable for local review or CI/CD publishing
- Keep configuration environment-driven instead of hard-coding one test environment

The goal is not simply to make requests. The goal is to make failures understandable, coverage intentional, and the framework easy to extend.

## What Is Covered

| Area | Examples of coverage |
|---|---|
| Public API | Status and demo-statistics endpoints without authentication |
| Authentication | Successful login, invalid credentials, bearer-token handling |
| Application CRUD | Create, list, update, and delete applications |
| Application summaries | Counts by workflow status and total applications |
| Field updates | Notes, remote type, salary range, and status changes |
| Negative testing | Missing required fields, invalid statuses, unauthorized access, not-found responses |
| Parametrized testing | Supported statuses and valid/invalid status transitions |
| Audit logging | Create, update, and delete operations recorded correctly |
| API-key security | Verifies generated keys are not stored as plain text |

The source-of-truth test cases are available in [`docs/test-cases-job-tracker-api.csv`](docs/test-cases-job-tracker-api.csv), and the API contract is available in [`docs/job-tracker-api-openapi.json`](docs/job-tracker-api-openapi.json).

## Technology Stack

- **Python 3** — test implementation and framework utilities
- **pytest** — test discovery, fixtures, markers, parameterization, and assertions
- **Requests** — HTTP communication with the API
- **SQLite** — direct persistence checks for selected security and audit scenarios
- **pytest-html** — self-contained human-readable reports
- **JUnit XML** — CI/CD-compatible test results
- **Shell, PowerShell, and batch runners** — cross-platform execution helpers

## Project Structure

```text
.
├── clients/                         # Reusable HTTP and SQLite clients
├── configs/                         # Environment-driven settings
├── docs/                            # Test cases, OpenAPI contract, checkpoints
├── helpers/                         # Authentication, payload, and error helpers
├── tests/
│   ├── api-keys/                    # API-key persistence/security checks
│   ├── applications/                # Core application workflow tests
│   ├── applications_audit_logs/     # Database-backed audit-log checks
│   ├── applications_negative/       # Validation and error-path tests
│   ├── applications_parametrized/   # Data-driven status tests
│   ├── auth/                        # Login tests
│   └── public/                      # Unauthenticated endpoint tests
├── reports/                         # Timestamped generated reports
├── conftest.py                      # Custom pytest options and TCID filtering
├── pytest.ini                       # Pytest logging and marker configuration
├── run_tests.py                     # Cross-platform test runner
├── run_tests.sh                     # macOS/Linux runner
├── run_tests.ps1                    # PowerShell runner
├── run_tests.bat                    # Windows Command Prompt runner
└── requirements.txt                 # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.9 or newer
- A locally running copy of the [application under test](https://github.com/supersqa1/job-tracker-app-for-testing)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/supersqa1/job-tracker-app-api-testing.git
cd job-tracker-app-api-testing
```

### 2. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application under test

Follow the application repository’s startup instructions. The course-friendly default is:

```bash
./run-app.sh
```

Confirm the API is available at `http://localhost:3050` and that Swagger loads at `http://localhost:3050/docs`.

## Running the Tests

The recommended runner creates a unique report directory for each execution:

```bash
./run_tests.sh
```

The equivalent Python command is:

```bash
python run_tests.py
```

On Windows, use either `run_tests.bat` or `run_tests.ps1`.

### Environment configuration

The framework supports these environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `BASE_URL` | `http://localhost:3050` | API host and port |
| `DEFAULT_USER_EMAIL` | `student@example.com` | Login user used by authenticated tests |
| `DEFAULT_USER_PASSWORD` | `Password123!` | Login password used by authenticated tests |
| `DATABASE_PATH` | Local course database path | SQLite file used by direct database assertions |

For a different environment:

```bash
BASE_URL=http://localhost:3060 ./run_tests.sh
```

Or pass the URL directly to the runner:

```bash
./run_tests.sh --base-url http://localhost:3060
```

The API-key storage test reads the SQLite database directly. Set `DATABASE_PATH` to the database created by your local application copy if its location differs from the default.

## Useful Commands

Run a feature folder:

```bash
./run_tests.sh tests/applications
```

Run one test file:

```bash
./run_tests.sh tests/auth/test_verify_login.py
```

Run tests by keyword:

```bash
./run_tests.sh -k login
./run_tests.sh -k "application and not audit"
```

Run tests by test-case ID:

```bash
./run_tests.sh --tcid 003
./run_tests.sh --tcid 007 --tcid 013
```

List all available IDs:

```bash
./run_tests.sh --list-tcids
```

Stop after the first failure and show verbose output:

```bash
./run_tests.sh --maxfail=1 -vv
```

Preview the generated pytest command without executing tests:

```bash
./run_tests.sh --dry-run
```

## Example Test Flow

The framework supports end-to-end API workflows, not only single-request checks. A typical authenticated application test follows this pattern:

```python
from clients.api_client import APIClient


def test_user_can_create_application():
    client = APIClient()  # Logs in and stores the bearer token

    payload = {
        "company_name": "Example Company",
        "role_title": "QA Engineer",
        "status": "potential",
    }

    created = client.post_json(
        "/api/v1/applications",
        data=payload,
        expected_status_code=201,
    )

    assert created["company_name"] == payload["company_name"]
    assert created["status"] == payload["status"]
```

The reusable `APIClient` centralizes URL construction, authentication headers, request logging, JSON parsing, and status-code validation. Feature-specific helpers keep test intent readable while preserving explicit assertions.

## Reports and Test Artifacts

Every `run_tests.py` execution creates a timestamped directory under `reports/` containing:

- `report.html` — self-contained HTML report for human review
- `junit.xml` — machine-readable results for CI/CD systems
- `run-summary.json` — command, environment, report locations, and exit code

For example:

```text
reports/20260824_143012/
├── report.html
├── junit.xml
└── run-summary.json
```

Existing reports in the repository are examples of the generated output; new local runs should be reviewed from their newly created timestamped directory.

## Test Design

The suite uses several complementary techniques:

- **Contract-oriented assertions** validate status codes, required fields, types, and response structure.
- **Workflow tests** create data, retrieve it, update it, and clean it up through the public API.
- **Negative tests** confirm the API rejects malformed, unauthorized, and nonexistent requests predictably.
- **Parametrization** covers multiple valid statuses and transitions without duplicating test logic.
- **Custom TCIDs** connect automated tests to the documented test-case inventory.
- **Database assertions** verify important persistence behavior that cannot be proven from the API response alone.

## Learning Outcomes

This project is a practical record of building API-testing skills incrementally—from public GET requests and login tests to reusable clients, protected endpoints, negative testing, data-driven scenarios, audit logs, and persistence validation.

It is especially useful for demonstrating understanding of:

- REST request and response behavior
- Authentication and authorization boundaries
- CRUD and business-workflow testing
- API error contracts
- Test maintainability and reuse
- Test data design and cleanup
- Reporting for developers and CI/CD pipelines

## Roadmap

Potential next improvements include:

- Add CI execution with published HTML/JUnit artifacts
- Introduce fixtures for isolated test data and cleanup
- Add schema validation against the OpenAPI document
- Add API-key-authenticated request coverage
- Expand rate-limit and health-check scenarios
- Add retry/diagnostic behavior for environment readiness
- Publish trend metrics for pass rate and endpoint coverage

## Related Projects

- **System under test:** [SuperSQA Job Tracker course application](https://github.com/supersqa1/job-tracker-app-for-testing)
- **Application portfolio project:** [SuperSQA Job Tracker](https://github.com/supersqa1/supersqa-job-tracker)
- **Automation portfolio project:** [Job Tracker API Test Automation](https://github.com/supersqa1/job-tracker-app-api-testing)

If you are reviewing this repository as part of a QA or software-engineering portfolio, the fastest way to explore it is to inspect the [test inventory](docs/test-cases-job-tracker-api.csv), run `./run_tests.sh --list-tcids`, and open the generated HTML report after a local test run.
