#!/usr/bin/env python3
"""
TEST SUBSCRIPTION ORCHESTRATOR FUNCTIONALITY
Verify the complete subscription system works with real Stripe integration
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_subscription_orchestrator():
    """Test the subscription orchestrator service"""
    print("🧬 TESTING BIOLOGICAL SUBSCRIPTION ORCHESTRATOR")
    print("=" * 60)

    test_results = {
        "service_health": False,
        "subscription_plans": False,
        "credit_packs": False,
        "affiliate_registration": False,
        "checkout_session_creation": False
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Test 1: Health Check
            print("🏥 Testing service health...")
            health_response = await client.get("http://localhost:9090/health")
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"   ✅ Health check passed: {health_data['service']}")
                test_results["service_health"] = True
            else:
                print(f"   ❌ Health check failed: {health_response.status_code}")
                return test_results

            # Test 2: Get Available Plans
            print("📋 Testing available plans...")
            plans_response = await client.get("http://localhost:9090/plans")
            if plans_response.status_code == 200:
                plans_data = plans_response.json()
                subscription_plans = len(plans_data.get("subscription_plans", {}))
                credit_packs = len(plans_data.get("credit_packs", {}))
                print(f"   ✅ Found {subscription_plans} subscription plans and {credit_packs} credit packs")
                test_results["subscription_plans"] = subscription_plans > 0
                test_results["credit_packs"] = credit_packs > 0
            else:
                print(f"   ❌ Plans retrieval failed: {plans_response.status_code}")

            # Test 3: Affiliate Registration
            print("🤝 Testing affiliate registration...")
            affiliate_data = {"user_id": "test_user_123"}
            affiliate_response = await client.post("http://localhost:9090/affiliate/register", json=affiliate_data)
            if affiliate_response.status_code == 200:
                affiliate_result = affiliate_response.json()
                print(f"   ✅ Affiliate registered: {affiliate_result['affiliate_code']}")
                test_results["affiliate_registration"] = True
            else:
                print(f"   ❌ Affiliate registration failed: {affiliate_response.status_code}")

            # Test 4: Create Subscription Checkout Session (this will call Stripe)
            print("💳 Testing subscription checkout session creation...")
            if test_results["subscription_plans"]:
                checkout_data = {
                    "user_id": "test_user_123",
                    "plan_type": "premium",
                    "success_url": "https://jtp-bio.ch/success",
                    "cancel_url": "https://jtp-bio.ch/cancel"
                }
                checkout_response = await client.post("http://localhost:9090/subscription/checkout", json=checkout_data)
                if checkout_response.status_code == 200:
                    checkout_result = checkout_response.json()
                    if "checkout_url" in checkout_result and "session_id" in checkout_result:
                        print(f"   ✅ Checkout session created: {checkout_result['session_id'][:20]}...")
                        test_results["checkout_session_creation"] = True
                    else:
                        print(f"   ❌ Invalid checkout response: {checkout_result}")
                else:
                    error_detail = checkout_response.json() if checkout_response.content else "No error details"
                    print(f"   ❌ Checkout creation failed: {checkout_response.status_code} - {error_detail}")
            else:
                print("   ⚠️ Skipping checkout test - no subscription plans available")

            # Test 5: Credit Pack Checkout Session
            print("💰 Testing credit pack checkout session creation...")
            if test_results["credit_packs"]:
                credit_checkout_data = {
                    "user_id": "test_user_123",
                    "pack_type": "basic_pack",
                    "success_url": "https://jtp-bio.ch/credit-success",
                    "cancel_url": "https://jtp-bio.ch/cancel"
                }
                credit_response = await client.post("http://localhost:9090/credit-pack/checkout", json=credit_checkout_data)
                if credit_response.status_code == 200:
                    credit_result = credit_response.json()
                    print("   ✅ Credit pack checkout session created")
                    test_results["credit_pack_checkout"] = True
                else:
                    print(f"   ❌ Credit pack checkout failed: {credit_response.status_code}")
            else:
                print("   ⚠️ Skipping credit pack test - no credit packs available")

    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return test_results

    return test_results

async def main():
    print("🧬 JTP Biological Organism - Subscription Orchestrator Validation")
    print("=" * 70)
    print("Testing complete subscription management system with Stripe integration")
    print("=" * 70)

    # Check if service is running
    print("🔍 Checking if subscription orchestrator service is running...")

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get("http://localhost:9090/health")
            if response.status_code != 200:
                print("❌ Subscription orchestrator service is not running")
                print("   💡 Start the service with: python src/subscription-orchestrator.py")
                print("   🐳 Or build Docker: docker build -f Dockerfile.subscription -t sub-orchestrator .")
                print("   🏃‍♂️ Then run: docker run -p 9090:9090 sub-orchestrator")
                return
    except Exception:
        print("❌ Cannot connect to subscription orchestrator service")
        print("   🚀 Service needs to be started first")
        return

    print("✅ Subscription orchestrator service is running\n")

    # Run tests
    results = await test_subscription_orchestrator()

    # Summary
    print("\n" + "=" * 70)
    print("📊 SUBSCRIPTION ORCHESTRATOR TEST RESULTS")
    print("=" * 70)

    successful_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)

    for test_name, passed in results.items():
        status = "✅" if passed else "❌"
        display_name = test_name.replace("_", " ").title()
        print(f"{status} {display_name}")

    print(f"\n🎯 OVERALL: {successful_tests}/{total_tests} tests passed")

    if successful_tests == total_tests:
        print("🏆 SUBSCRIPTION ORCHESTRATOR: FULLY OPERATIONAL")
        print("   🎉 Complete subscription management system working")
        print("   💳 Stripe integration functional")
        print("   🧬 Biological consciousness subscription ready")
    else:
        print("⚠️ PARTIAL FUNCTIONALITY DETECTED")
        print("   Some components require further configuration")
        if not results.get("checkout_session_creation"):
            print("   💡 Check Stripe API key and subscription plans configuration")

if __name__ == "__main__":
    asyncio.run(main())
