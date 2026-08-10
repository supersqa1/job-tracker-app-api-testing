#!/usr/bin/env python3
"""
Pytest runner for the Job Tracker API test suite.

The runner keeps pytest's normal selection behavior while adding consistent,
timestamped report output for local runs and CI/CD pipelines.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_TEST_TARGET = "tests"
DEFAULT_REPORT_ROOT = "reports"


EPILOG = """
Examples:
  Run all tests:
    python run_tests.py

  Run a test by custom test case id:
    python run_tests.py --tcid 001

  Run multiple test case ids:
    python run_tests.py --tcid 001 --tcid 003
    python run_tests.py --tcid 001,003,007

  List available custom test case ids:
    python run_tests.py --list-tcids

  Run tests by partial test name, same as pytest -k:
    python run_tests.py -k login
    python run_tests.py -k "login and not invalid"

  Run tests by file or folder:
    python run_tests.py tests/auth/test_verify_login.py
    python run_tests.py tests/public

  Pass extra pytest options:
    python run_tests.py -k login -vv
    python run_tests.py tests/auth/test_verify_login.py --maxfail=1

  Use a different API base URL for CI/CD:
    python run_tests.py --base-url https://staging.example.com

  Force a specific Python interpreter:
    python run_tests.py --python .venv/bin/python

Reports:
  Every run creates a unique folder under reports/, for example:
    reports/20260809_143012/

  That folder includes:
    report.html      pytest-html report
    junit.xml        JUnit XML report for CI/CD test publishing
    run-summary.json command, environment, report paths, and exit code
"""


def parse_args(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        prog="run_tests.py",
        description=(
            "Run the Job Tracker API pytest suite with convenient selection "
            "options and timestamped reports."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )

    parser.add_argument(
        "targets",
        nargs="*",
        help=(
            "Optional pytest test target(s), such as a full test file, folder, "
            "or node id. Defaults to tests/."
        ),
    )
    parser.add_argument(
        "--tcid",
        action="append",
        default=[],
        metavar="ID[,ID...]",
        help=(
            "Run tests with matching @pytest.mark.tcid values. Can be repeated "
            "or provided as a comma-separated list."
        ),
    )
    parser.add_argument(
        "--list-tcids",
        action="store_true",
        help="List discovered @pytest.mark.tcid values and exit without running tests.",
    )
    parser.add_argument(
        "-k",
        dest="keyword",
        metavar="EXPRESSION",
        help="Run tests matching a pytest -k keyword expression.",
    )
    parser.add_argument(
        "--report-root",
        default=DEFAULT_REPORT_ROOT,
        help=f"Folder where timestamped report directories are created. Default: {DEFAULT_REPORT_ROOT}",
    )
    parser.add_argument(
        "--report-prefix",
        default="",
        help="Optional prefix for the timestamped report folder name, such as smoke or staging.",
    )
    parser.add_argument(
        "--base-url",
        help="Set BASE_URL for this run without exporting it in the shell.",
    )
    parser.add_argument(
        "--python",
        dest="python_executable",
        help=(
            "Python executable used to launch pytest. Defaults to the active "
            "interpreter, or .venv/bin/python when no virtualenv is active."
        ),
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="Set an environment variable for this run. Can be repeated.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the pytest command and report paths without running tests.",
    )

    return parser.parse_known_args(argv)


def split_tcids(values: Iterable[str]) -> list[str]:
    tcids: list[str] = []
    for value in values:
        for item in value.split(","):
            tcid = item.strip()
            if tcid:
                tcids.append(tcid)
    return tcids


def iter_tcid_marks(tree: ast.AST) -> Iterable[tuple[str, str]]:
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            func = decorator.func
            is_tcid_marker = (
                isinstance(func, ast.Attribute)
                and func.attr == "tcid"
                and isinstance(func.value, ast.Attribute)
                and func.value.attr == "mark"
                and isinstance(func.value.value, ast.Name)
                and func.value.value.id == "pytest"
            )
            if not is_tcid_marker or not decorator.args:
                continue
            tcid_arg = decorator.args[0]
            if isinstance(tcid_arg, ast.Constant) and isinstance(tcid_arg.value, str):
                yield tcid_arg.value, node.name


def discover_tcids() -> dict[str, list[tuple[Path, str]]]:
    discovered: dict[str, list[tuple[Path, str]]] = {}
    for test_file in sorted((PROJECT_ROOT / DEFAULT_TEST_TARGET).rglob("test_*.py")):
        try:
            tree = ast.parse(test_file.read_text(encoding="utf-8"), filename=str(test_file))
        except SyntaxError:
            continue

        for tcid, test_name in iter_tcid_marks(tree):
            discovered.setdefault(tcid, []).append((test_file, test_name))

    return discovered


def print_discovered_tcids(discovered: dict[str, list[tuple[Path, str]]]) -> None:
    if not discovered:
        print("No @pytest.mark.tcid values were found.")
        return

    print("Discovered TCIDs:")
    for tcid in sorted(discovered):
        for test_file, test_name in discovered[tcid]:
            relative_file = test_file.relative_to(PROJECT_ROOT)
            print(f"  {tcid}: {relative_file}::{test_name}")


def targets_for_tcids(tcids: list[str], discovered: dict[str, list[tuple[Path, str]]]) -> list[str]:
    targets: list[str] = []
    seen: set[str] = set()
    for tcid in tcids:
        for test_file, _test_name in discovered.get(tcid, []):
            relative_file = str(test_file.relative_to(PROJECT_ROOT))
            if relative_file not in seen:
                targets.append(relative_file)
                seen.add(relative_file)
    return targets


def build_report_dir(report_root: str, report_prefix: str) -> Path:
    root = (PROJECT_ROOT / report_root).resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = report_prefix.strip().replace(" ", "_")
    base_name = f"{prefix}_{timestamp}" if prefix else timestamp
    report_dir = root / base_name

    suffix = 1
    while report_dir.exists():
        report_dir = root / f"{base_name}_{suffix:02d}"
        suffix += 1

    return report_dir


def parse_env_overrides(values: Iterable[str]) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"--env must use NAME=VALUE format. Got: {value}")
        name, env_value = value.split("=", 1)
        name = name.strip()
        if not name:
            raise ValueError(f"--env variable name cannot be empty. Got: {value}")
        overrides[name] = env_value
    return overrides


def select_python_executable(requested_python: str | None) -> str:
    if requested_python:
        return str((PROJECT_ROOT / requested_python).resolve()) if not Path(requested_python).is_absolute() else requested_python

    if os.getenv("VIRTUAL_ENV"):
        return sys.executable

    repo_venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
    if repo_venv_python.exists():
        return str(repo_venv_python)

    return sys.executable


def quote_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def write_summary(
    summary_path: Path,
    command: list[str],
    exit_code: int | None,
    report_dir: Path,
    html_report: Path,
    junit_report: Path,
    env_overrides: dict[str, str],
) -> None:
    summary = {
        "command": command,
        "command_text": quote_command(command),
        "exit_code": exit_code,
        "report_dir": str(report_dir),
        "html_report": str(html_report),
        "junit_report": str(junit_report),
        "env_overrides": env_overrides,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args, passthrough_args = parse_args(argv or sys.argv[1:])

    try:
        env_overrides = parse_env_overrides(args.env)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.base_url:
        env_overrides["BASE_URL"] = args.base_url

    selected_tcids = split_tcids(args.tcid)
    discovered_tcids = discover_tcids() if selected_tcids or args.list_tcids else {}
    if args.list_tcids:
        print_discovered_tcids(discovered_tcids)
        return 0

    report_dir = build_report_dir(args.report_root, args.report_prefix)
    html_report = report_dir / "report.html"
    junit_report = report_dir / "junit.xml"
    summary_path = report_dir / "run-summary.json"

    targets = args.targets
    if not targets and selected_tcids:
        targets = targets_for_tcids(selected_tcids, discovered_tcids)
        missing_tcids = sorted(set(selected_tcids) - set(discovered_tcids))
        if missing_tcids:
            print(f"Warning: no tests discovered for TCID(s): {', '.join(missing_tcids)}")
    if not targets:
        targets = [DEFAULT_TEST_TARGET]

    python_executable = select_python_executable(args.python_executable)
    command = [
        python_executable,
        "-m",
        "pytest",
        *targets,
    ]

    if args.keyword:
        command.extend(["-k", args.keyword])

    for tcid in selected_tcids:
        command.extend(["--tcid", tcid])

    command.extend(
        [
            f"--html={html_report}",
            "--self-contained-html",
            f"--junitxml={junit_report}",
        ]
    )
    command.extend(passthrough_args)

    print("Pytest runner")
    print(f"Project:    {PROJECT_ROOT}")
    print(f"Python:     {python_executable}")
    print(f"Reports:    {report_dir}")
    print(f"HTML:       {html_report}")
    print(f"JUnit XML:  {junit_report}")
    if env_overrides:
        print("Env:        " + ", ".join(f"{name}=***" if "PASSWORD" in name or "TOKEN" in name else f"{name}={value}" for name, value in env_overrides.items()))
    print(f"Command:    {quote_command(command)}", flush=True)

    if args.dry_run:
        print("Dry run only. No tests were executed.")
        return 0

    report_dir.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env.update(env_overrides)

    completed = subprocess.run(command, cwd=PROJECT_ROOT, env=env, check=False)
    write_summary(
        summary_path=summary_path,
        command=command,
        exit_code=completed.returncode,
        report_dir=report_dir,
        html_report=html_report,
        junit_report=junit_report,
        env_overrides=env_overrides,
    )

    print(f"Run summary: {summary_path}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
