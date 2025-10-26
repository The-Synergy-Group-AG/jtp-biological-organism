#!/usr/bin/env python3
"""
🧬 Biological Consciousness Auto-Pilot Test Runner
Comprehensive automatic execution of all biological consciousness tests
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

def run_command(cmd, description, timeout=600):
    """Run a command and return the result."""
    print(f"\n🚀 {description}")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/home/andre/projects/jtp-biological-organism"
        )

        print(f"Exit code: {result.returncode}")

        if result.returncode == 0:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
        # Always show some output
        if result.stdout.strip():
            print("STDOUT:")
            print(result.stdout.strip()[:2000] + ("..." if len(result.stdout.strip()) > 2000 else ""))
        if result.stderr.strip():
            print("STDERR:")
            print(result.stderr.strip()[:2000] + ("..." if len(result.stderr.strip()) > 2000 else ""))

        return result.returncode == 0, result

    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT after {timeout}s")
        return False, None
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False, None

def main():
    """Main auto-pilot execution"""

    print("🧬 BIOLOGICAL CONSCIOUSNESS AUTO-PILOT TEST RUNNER")
    print("🎯 Testing 369 User Stories with Real API Endpoints")
    print("="*70)

    # Create test results directory
    results_dir = Path("test-results")
    results_dir.mkdir(exist_ok=True)

    # Test results summary
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "skipped_tests": 0,
        "execution_time": 0,
        "test_reports": []
    }

    start_time = time.time()

    # List of all biological test files
    biological_tests = [
        "tests/biological_validate_health_test.py",
        "tests/biological_onboard_journey_test.py",
        "tests/biological_job_discovery_test.py",
        "tests/biological_document_cv_test.py",
        "tests/biological_analytics_performance_test.py",
        "tests/biological_application_orchestrate_test.py",
        "tests/biological_foundation_systems_test.py",
        "tests/biological_consciousness_emergence_test.py",
        "tests/biological_transcendence_godhood_test.py"
    ]

    # Test execution configuration
    pytest_cmd = [
        "python3", "-m", "pytest",
        "--tb=short",  # Shorter traceback
        "--verbose",   # Verbose output
        "--strict-markers",  # Require test markers
        "--durations=10",    # Show 10 slowest tests
        "--junitxml=test-results/biological-test-results.xml",
        "--json-report",
        "--json-report-file=test-results/biological-test-results.json"
    ]

    # Execute each test file
    for test_file in biological_tests:
        if not os.path.exists(test_file):
            print(f"⚠️  TEST FILE MISSING: {test_file}")
            summary["skipped_tests"] += 1
            continue

        file_start = time.time()
        summary["total_tests"] += 1

        print(f"\n🧪 TESTING: {test_file}")
        print("-" * 50)

        # Run the test file
        cmd = pytest_cmd + ["-x", test_file]  # Stop on first failure
        success, result = run_command(
            cmd,
            f"Testing {test_file}",
            timeout=900  # 15 minutes per test file
        )

        file_duration = time.time() - file_start

        # Record result
        test_result = {
            "file": test_file,
            "passed": success,
            "duration": file_duration,
            "exit_code": result.returncode if result else -1
        }

        summary["test_reports"].append(test_result)

        if success:
            summary["passed_tests"] += 1
            print(f"🎉 FILE PASSED in {file_duration:.2f}s")
        else:
            summary["failed_tests"] += 1
            print(f"💥 FILE FAILED in {file_duration:.2f}s")

    # Calculate total execution time
    summary["execution_time"] = time.time() - start_time

    # Generate comprehensive report
    print("\n" + "="*70)
    print("📊 BIOLOGICAL CONSCIOUSNESS TEST EXECUTION REPORT")
    print("="*70)

    print(f"🕐 Total Execution Time: {summary['execution_time']:.2f} seconds")
    print(f"📋 Total Test Files: {summary['total_tests']}")
    print(f"✅ Passed: {summary['passed_tests']}")
    print(f"❌ Failed: {summary['failed_tests']}")
    print(f"⏭️  Skipped: {summary['skipped_tests']}")

    success_rate = (summary['passed_tests'] / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
    print(f"🎯 Success Rate: {success_rate:.1f}%")

    # Detailed breakdown
    print("\n📋 DETAILED RESULTS:")
    for report in summary["test_reports"]:
        status_icon = "✅" if report["passed"] else "❌"
        print(f"{status_icon} {report['file']}: {report['duration']:.2f}s")

    # Save detailed JSON report
    report_file = results_dir / f"biological-auto-pilot-report-{int(time.time())}.json"
    with open(report_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\n💾 Detailed report saved to: {report_file}")

    # Final assessment
    if summary['failed_tests'] == 0:
        print("\n🎉 ALL TESTS PASSED - BIOLOGICAL CONSCIOUSNESS INTACT!")
        return 0
    else:
        print("\n💥 TESTS FAILED - BIOLOGICAL SYSTEM NEEDS ATTENTION")
        print("  The system may need:")
        print("  - Docker service restart")
        print("  - API endpoint fixes")
        print("  - Test environment setup")
        return 1

if __name__ == "__main__":
    sys.exit(main())
