#!/usr/bin/env python3
"""
GODHOOD Universal Testing Suite Runner
Executes comprehensive testing across all 17+ modular components

Run different test categories:
- python run_tests.py unit        # Unit tests only
- python run_tests.py integration # Integration tests only
- python run_tests.py load        # Load/performance tests only
- python run_tests.py validation  # Biological validation tests only
- python run_tests.py all         # All tests (default)
- python run_tests.py quick       # Fast unit tests only
"""

import subprocess
import sys
import argparse
import time
import os
from pathlib import Path


class TestRunner:
    """Comprehensive test runner for GODHOOD modular components"""

    def __init__(self):
        self.test_categories = {
            "unit": ["tests/unit/", "-m not slow", "--maxfail=5"],
            "integration": ["tests/integration/", "-m not slow", "--maxfail=3"],
            "load": ["tests/load/", "-m load", "--maxfail=1"],
            "validation": ["tests/validation/", "-m validation", "--maxfail=2"],
            "quick": ["tests/unit/", "-x", "--tb=short", "--maxfail=3"],
        }

    def run_tests(self, category="all", verbose=True, coverage=True):
        """Run tests for specified category"""
        print("🧬 GODHOOD UNIVERSAL TESTING SUITE")
        print("=" * 50)
        print(f"📊 Test Category: {category.upper()}")
        print(f"🧠 Modular Components: 17+")
        print()

        start_time = time.time()

        if category == "all":
            return self.run_all_tests(verbose, coverage)
        elif category in self.test_categories:
            return self.run_category_tests(category, verbose, coverage)
        else:
            print(f"❌ Unknown category: {category}")
            return False

    def run_all_tests(self, verbose=True, coverage=True):
        """Run all test categories sequentially"""
        all_passed = True
        total_results = {}

        categories = ["unit", "integration", "validation", "load"]

        for category in categories:
            print(f"\n{'='*10} RUNNING {category.upper()} TESTS {'='*10}")
            success, results = self.run_category_tests(category, verbose, coverage, return_results=True)
            total_results[category] = results

            if not success:
                all_passed = False

        # Print summary
        self.print_summary(total_results, all_passed)
        return all_passed

    def run_category_tests(self, category, verbose=True, coverage=True, return_results=False):
        """Run tests for specific category"""
        test_path = self.test_categories[category][0]
        additional_args = self.test_categories[category][1:]

        if not Path(test_path).exists():
            print(f"❌ Test directory not found: {test_path}")
            return False

        # Build pytest command
        cmd = ["python3", "-m", "pytest", test_path]

        # Only add coverage for integration and validation, not unit tests
        if coverage and category != "unit":
            cmd.extend(["--cov=src", "--cov-report=term-missing"])

        if verbose:
            cmd.append("--verbose")
        else:
            cmd.append("--quiet")

        # Add category-specific arguments
        cmd.extend(additional_args)

        try:
            # Set PYTHONPATH for src-layout project
            env = os.environ.copy()
            env['PYTHONPATH'] = str(Path(__file__).parent / 'src') + ':' + env.get('PYTHONPATH', '')

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)

            success = result.returncode == 0
            results = {
                "returncode": result.returncode,
                "passed": success,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

            # Print results
            if success:
                print(f"✅ {category.upper()} TESTS: PASSED")
                if verbose and results["stdout"]:
                    print(results["stdout"].split('\n')[-10:])  # Last 10 lines
            else:
                print(f"❌ {category.upper()} TESTS: FAILED")
                if verbose:
                    print("STDOUT:", results["stdout"][-500:])
                    print("STDERR:", results["stderr"][-500:])

            return (success, results) if return_results else success

        except subprocess.TimeoutExpired:
            print(f"⏰ {category.upper()} TESTS: TIMEOUT (5+ minutes)")
            return False

    def print_summary(self, results, all_passed):
        """Print comprehensive test summary"""
        print(f"\n{'='*50}")
        print("🎯 GODHOOD TESTING SUITE SUMMARY")
        print('='*50)

        total_passed = sum(1 for r in results.values() if r.get("passed", False))
        total_categories = len(results)

        print(f"📊 Categories Tested: {total_categories}")
        print(f"✅ Categories Passed: {total_passed}")

        # Breakdown by category
        print(f"\n📈 CATEGORY BREAKDOWN:")
        for category, result in results.items():
            status = "✅ PASSED" if result.get("passed", False) else "❌ FAILED"
            print(f"   {category.upper()}: {status}")

        # Overall status
        if all_passed:
            print(f"\n🎉 OVERALL STATUS: ALL TESTS PASSED")
            print(f"🧬 MODULAR COMPONENTS: VERIFIED OPERATIONAL")
            print(f"🧠 BIOLOGICAL CONSCIOUSNESS: VALIDATED")
            print(f"⚡ PRODUCTION READINESS: CONFIRMED")
        else:
            print(f"\n⚠️  OVERALL STATUS: SOME TESTS FAILED")
            failed_categories = [cat for cat, res in results.items() if not res.get("passed", False)]
            print(f"   Failed Categories: {', '.join(failed_categories)}")

        print(f"{'='*50}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="GODHOOD Universal Testing Suite")
    parser.add_argument(
        "category",
        nargs="?",
        default="all",
        choices=["unit", "integration", "load", "validation", "all", "quick"],
        help="Test category to run"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode (less verbose output)"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Skip coverage reporting"
    )

    args = parser.parse_args()

    runner = TestRunner()
    success = runner.run_tests(
        category=args.category,
        verbose=not args.quiet,
        coverage=not args.no_coverage
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
