#!/usr/bin/env bash
#
# Shell wrapper for the Job Tracker API pytest runner.
#
# This script keeps the same user-facing behavior as run_tests.py while giving
# macOS/Linux users a shorter command for local runs and CI/CD jobs.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_RUNNER="${SCRIPT_DIR}/run_tests.py"

show_help() {
  cat <<'EOF'
Job Tracker API Test Runner

Usage:
  ./run_tests.sh [options] [pytest-targets] [pytest-options]

Common options:
  -h, --help                  Show this help message.
  --tcid ID[,ID...]           Run tests by custom @pytest.mark.tcid value.
                              Can be repeated.
  --list-tcids                List discovered TCIDs and exit.
  -k EXPRESSION               Run tests matching a pytest -k expression.
  --report-root DIR           Folder for timestamped report directories.
                              Default: reports
  --report-prefix PREFIX      Prefix the timestamped report folder name.
  --base-url URL              Set BASE_URL for this run.
  --env NAME=VALUE            Set an environment variable for this run.
                              Can be repeated.
  --python PATH               Python executable used by the Python runner.
  --dry-run                   Print the pytest command without running tests.

Examples:
  Run all tests:
    ./run_tests.sh

  Run a test by custom test case id:
    ./run_tests.sh --tcid 001

  Run multiple test case ids:
    ./run_tests.sh --tcid 001 --tcid 003
    ./run_tests.sh --tcid 001,003,007

  List available custom test case ids:
    ./run_tests.sh --list-tcids

  Run tests by partial test name, same as pytest -k:
    ./run_tests.sh -k login
    ./run_tests.sh -k "login and not invalid"

  Run tests by file or folder:
    ./run_tests.sh tests/auth/test_verify_login.py
    ./run_tests.sh tests/public

  Pass extra pytest options:
    ./run_tests.sh -k login -vv
    ./run_tests.sh tests/auth/test_verify_login.py --maxfail=1

  Use a different API base URL for CI/CD:
    ./run_tests.sh --base-url https://staging.example.com

Reports:
  The underlying Python runner creates a unique timestamped folder under
  reports/ with:
    report.html
    junit.xml
    run-summary.json
EOF
}

if [[ ! -f "${PYTHON_RUNNER}" ]]; then
  echo "Error: run_tests.py was not found next to run_tests.sh." >&2
  exit 1
fi

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  show_help
  exit 0
fi

PYTHON_BIN="${PYTHON:-python3}"

exec "${PYTHON_BIN}" "${PYTHON_RUNNER}" "$@"
