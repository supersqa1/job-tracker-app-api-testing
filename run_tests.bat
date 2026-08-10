@echo off
setlocal

rem Windows Command Prompt wrapper for the Job Tracker API pytest runner.
rem Delegates to run_tests.py so report generation and test selection stay
rem identical across platforms.

set "SCRIPT_DIR=%~dp0"
set "PYTHON_RUNNER=%SCRIPT_DIR%run_tests.py"

if not exist "%PYTHON_RUNNER%" (
  echo Error: run_tests.py was not found next to run_tests.bat. 1>&2
  exit /b 1
)

if /I "%~1"=="-h" goto help
if /I "%~1"=="--help" goto help

if defined PYTHON (
  "%PYTHON%" "%PYTHON_RUNNER%" %*
  exit /b %ERRORLEVEL%
)

python "%PYTHON_RUNNER%" %*
if %ERRORLEVEL% EQU 9009 (
  py -3 "%PYTHON_RUNNER%" %*
  exit /b %ERRORLEVEL%
)

exit /b %ERRORLEVEL%

:help
echo Job Tracker API Test Runner
echo.
echo Usage:
echo   run_tests.bat [options] [pytest-targets] [pytest-options]
echo.
echo Common options:
echo   -h, --help                  Show this help message.
echo   --tcid ID[,ID...]           Run tests by custom @pytest.mark.tcid value.
echo                               Can be repeated.
echo   --list-tcids                List discovered TCIDs and exit.
echo   -k EXPRESSION               Run tests matching a pytest -k expression.
echo   --report-root DIR           Folder for timestamped report directories.
echo                               Default: reports
echo   --report-prefix PREFIX      Prefix the timestamped report folder name.
echo   --base-url URL              Set BASE_URL for this run.
echo   --env NAME=VALUE            Set an environment variable for this run.
echo                               Can be repeated.
echo   --python PATH               Python executable used by the Python runner.
echo   --dry-run                   Print the pytest command without running tests.
echo.
echo Examples:
echo   Run all tests:
echo     run_tests.bat
echo.
echo   Run a test by custom test case id:
echo     run_tests.bat --tcid 001
echo.
echo   Run multiple test case ids:
echo     run_tests.bat --tcid 001 --tcid 003
echo     run_tests.bat --tcid 001,003,007
echo.
echo   List available custom test case ids:
echo     run_tests.bat --list-tcids
echo.
echo   Run tests by partial test name, same as pytest -k:
echo     run_tests.bat -k login
echo     run_tests.bat -k "login and not invalid"
echo.
echo   Run tests by file or folder:
echo     run_tests.bat tests\auth\test_verify_login.py
echo     run_tests.bat tests\public
echo.
echo   Pass extra pytest options:
echo     run_tests.bat -k login -vv
echo     run_tests.bat tests\auth\test_verify_login.py --maxfail=1
echo.
echo   Use a different API base URL for CI/CD:
echo     run_tests.bat --base-url https://staging.example.com
echo.
echo Reports:
echo   The underlying Python runner creates a unique timestamped folder under
echo   reports\ with:
echo     report.html
echo     junit.xml
echo     run-summary.json
exit /b 0
