<#
.SYNOPSIS
Runs the Job Tracker API pytest suite.

.DESCRIPTION
PowerShell wrapper for run_tests.py. It keeps test selection, timestamped HTML
reports, JUnit XML output, and CI/CD exit codes identical across platforms.

.EXAMPLE
.\run_tests.ps1

.EXAMPLE
.\run_tests.ps1 --tcid 001

.EXAMPLE
.\run_tests.ps1 -k "login and not invalid"

.EXAMPLE
.\run_tests.ps1 tests\auth\test_verify_login.py --maxfail=1
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonRunner = Join-Path $ScriptDir "run_tests.py"

function Show-RunnerHelp {
    @"
Job Tracker API Test Runner

Usage:
  .\run_tests.ps1 [options] [pytest-targets] [pytest-options]

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
    .\run_tests.ps1

  Run a test by custom test case id:
    .\run_tests.ps1 --tcid 001

  Run multiple test case ids:
    .\run_tests.ps1 --tcid 001 --tcid 003
    .\run_tests.ps1 --tcid 001,003,007

  List available custom test case ids:
    .\run_tests.ps1 --list-tcids

  Run tests by partial test name, same as pytest -k:
    .\run_tests.ps1 -k login
    .\run_tests.ps1 -k "login and not invalid"

  Run tests by file or folder:
    .\run_tests.ps1 tests\auth\test_verify_login.py
    .\run_tests.ps1 tests\public

  Pass extra pytest options:
    .\run_tests.ps1 -k login -vv
    .\run_tests.ps1 tests\auth\test_verify_login.py --maxfail=1

  Use a different API base URL for CI/CD:
    .\run_tests.ps1 --base-url https://staging.example.com

Reports:
  The underlying Python runner creates a unique timestamped folder under
  reports\ with:
    report.html
    junit.xml
    run-summary.json
"@
}

if ($args.Count -gt 0 -and ($args[0] -eq "--help" -or $args[0] -eq "-h")) {
    Show-RunnerHelp
    exit 0
}

if (-not (Test-Path -LiteralPath $PythonRunner)) {
    Write-Error "run_tests.py was not found next to run_tests.ps1."
    exit 1
}

$PythonCommand = if ($env:PYTHON) { $env:PYTHON } else { "python" }

& $PythonCommand $PythonRunner @args
$ExitCode = $LASTEXITCODE

if ($ExitCode -eq 9009 -and -not $env:PYTHON) {
    & py -3 $PythonRunner @args
    $ExitCode = $LASTEXITCODE
}

exit $ExitCode
