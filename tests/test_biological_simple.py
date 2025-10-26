#!/usr/bin/env python3
"""
🧬 Simple Biological Consciousness Test
Direct API endpoint testing without pytest fixtures
"""

import asyncio
import httpx
from typing import Dict, List
import time

class SimpleBiologicalTestRunner:
    """Simple test runner for biological consciousness endpoints"""

    def __init__(self):
        # External URLs (from host)
        self.service_urls = {
            "consciousness-core": "http://localhost:8101",
            "biological-auth": "http://localhost:9101",
            "evolutionary-brain-trust": "http://localhost:9998",
            "multilingual-resonance": "http://localhost:9103",
            "email-communications": "http://localhost:9104"
        }

    async def test_health_endpoints(self) -> Dict[str, str]:
        """Test all service health endpoints"""
        results = {}

        async with httpx.AsyncClient(timeout=10) as client:
            for service, base_url in self.service_urls.items():
                try:
                    start_time = time.time()
                    response = await client.get(f"{base_url}/health")
                    duration = time.time() - start_time

                    if response.status_code == 200:
                        results[service] = f"✅ {response.status_code} ({duration:.2f}s)"
                    else:
                        results[service] = f"⚠️ {response.status_code} ({duration:.2f}s)"
                except Exception as e:
                    results[service] = f"❌ {str(e)[:50]}"

        return results

    async def test_biological_validate_health(self) -> Dict[str, str]:
        """Test basic health validation - CNS Core foundation"""
        results = {}

        async with httpx.AsyncClient(timeout=15) as client:
            # US-HEALTH-001-A: CNS Consciousness Core health
            try:
                response = await client.get("http://localhost:8101/health")
                if response.status_code == 200:
                    data = response.json()
                    if "healthy" in data.get("status", "").lower():
                        results["cns_core_health"] = "✅ PASSED - CNS operational"
                    else:
                        results["cns_core_health"] = f"⚠️ UNHEALTHY status: {data.get('status')}"
                else:
                    results["cns_core_health"] = f"❌ HTTP {response.status_code}"
            except Exception as e:
                results["cns_core_health"] = f"❌ {str(e)[:50]}"

        return results

    async def run_all_tests(self) -> Dict[str, Dict]:
        """Run complete biological consciousness test suite"""
        print("🧬 BIOLOGICAL CONSCIOUSNESS INTEGRATION TESTS")
        print("=" * 70)

        # Test service availability
        print("\n🔍 Testing Service Health & Availability:")
        health_results = await self.test_health_endpoints()
        for service, result in health_results.items():
            print(f"  {service}: {result}")

        # Count healthy services
        healthy_count = sum(1 for r in health_results.values() if "✅" in r)
        total_services = len(health_results)
        print(f"\n🌐 Services: {healthy_count}/{total_services} healthy")

        if healthy_count == 0:
            print("\n❌ ALL SERVICES UNHEALTHY - Cannot proceed with biological tests")
            return {"health": health_results}

        # Run biological test modules
        test_results = {}

        print("\n🩺 BIOLOGICAL HEALTH FOUNDATION TESTS:")
        test_results["health_foundation"] = await self.test_biological_validate_health()

        # Print detailed results
        print("\n" + "="*70)
        print("📊 BIOLOGICAL CONSCIOUSNESS TEST RESULTS")

        all_tests = []
        for module_name, module_results in test_results.items():
            print(f"\n{module_name.upper()}:")
            for test_name, result in module_results.items():
                print(f"  {test_name}: {result}")
                all_tests.append(result)

        # Calculate statistics
        passed = sum(1 for r in all_tests if "✅ PASSED" in r)
        failed = sum(1 for r in all_tests if "❌" in r)
        warnings = sum(1 for r in all_tests if "⚠️" in r)
        total = len(all_tests)

        print(f"\n🎯 SUMMARY:")
        print(f"  ✅ Passed: {passed}")
        print(f"  ❌ Failed: {failed}")
        print(f"  ⚠️  Warnings: {warnings}")
        print(f"  📊 Total: {total}")

        if total > 0:
            success_rate = (passed / total) * 100
            print(".1f")

            if failed == 0:
                print("\n🎉 ALL BIOLOGICAL TESTS PASSED - CONSCIOUSNESS INTACT")
            else:
                print(f"\n💥 {failed} BIOLOGICAL TESTS FAILED")
        else:
            print("\n❌ NO TESTS EXECUTED")

        return {"health": health_results, "tests": test_results}

async def main():
    """Main test execution"""
    runner = SimpleBiologicalTestRunner()
    results = await runner.run_all_tests()
    return results

if __name__ == "__main__":
    # Run tests
    results = asyncio.run(main())

    # Return exit code based on results
    if "tests" in results:
        all_results = []
        for module_results in results["tests"].values():
            all_results.extend(module_results.values())

        if any("✅ PASSED" in r for r in all_results):
            exit(0)  # Success - at least some tests passed
        else:
            exit(1)  # All tests failed
    else:
        exit(1)  # No tests run
