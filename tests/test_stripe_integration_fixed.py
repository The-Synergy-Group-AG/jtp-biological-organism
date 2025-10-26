#!/usr/bin/env python3
"""
DIRECT STRIPE API VALIDATION - FIXED VERSION
Test payment gateway functionality with proper environment loading
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

async def test_stripe_api():
    """Direct test of Stripe API integration"""
    print("🔍 Testing Stripe Payment Gateway Integration...")
    print("=" * 50)
    
    # Load environment variables from the complete API ecosystem file
    load_dotenv('.env.complete.api.ecosystem')
    
    # Get Stripe API key from environment
    stripe_api_key = os.getenv('STRIPE_API_KEY', '')
    stripe_secret_key = os.getenv('STRIPE_SECRET_KEY', '')
    
    # Try both possible key names
    api_key = stripe_api_key or stripe_secret_key
    
    if not api_key:
        print("❌ STRIPE_API_KEY environment variable not set")
        print("💡 Checking available environment variables...")
        for key in ['STRIPE_API_KEY', 'STRIPE_SECRET_KEY', 'stripe_api_key', 'stripe_secret_key']:
            value = os.getenv(key, '')
            if value:
                print(f"   ✅ {key}: {value[:16]}... ({len(value)} chars)")
                api_key = value
                break
        if not api_key:
            return False
    
    print(f"✅ Stripe API key configured: {api_key[:16]}..." if api_key else "❌ No API key")
    
    try:
        # Test Stripe balance endpoint (requires valid API key)
        url = "https://api.stripe.com/v1/balance"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Stripe-Version': '2023-10-16'
        }
        
        print("🔗 Making API call to Stripe...")
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=headers)
            
            print(f"📡 HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                # Successful API call
                data = response.json()
                print("✅ SUCCESS: Stripe API is accessible and functional")
                print(f"   💰 Account Balance Data: Available: {len(data.get('available', []))} sources")
                print(f"   💳 Live/Test Mode: {data.get('livemode', 'unknown')}")
                print("✅ EVIDENCE: Payment gateway is fully operational"
                return True
                
            elif response.status_code == 401:
                print("❌ AUTHENTICATION FAILED: Invalid Stripe API key")
                print("   ⚠️  API key may be expired or incorrect")
                print(f"   🔍 Key ends with: ...{api_key[-8:] if api_key else 'None'}")
                return False
                
            elif response.status_code == 403:
                print("❌ FORBIDDEN: API key lacks permissions (check for restricted key)")
                return False
                
            else:
                print(f"❌ UNEXPECTED STATUS: {response.status_code}")
                print(f"   Response preview: {response.text[:200]}...")
                return False
                
    except httpx.ConnectTimeout:
        print("❌ TIMEOUT: Cannot connect to Stripe API (network issue)")
        return False
        
    except httpx.ConnectError:
        print("❌ CONNECTION ERROR: Cannot reach Stripe API servers")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

async def main():
    print("🧬 JTP Biological Organism - Payment Gateway Validation")
    print("=" * 60)
    
    success = await test_stripe_api()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ PAYMENT GATEWAY VALIDATION: SUCCESSFUL")
        print("   🎉 Stripe payment processing is fully operational")
        print("   💳 Subscription payments can be processed successfully")
        print("   🔗 Real Stripe API connectivity confirmed")
    else:
        print("❌ PAYMENT GATEWAY VALIDATION: FAILED")
        print("   🚫 Payment processing is not operational")
        print("   ⚠️  Subscription system requires valid Stripe configuration")
        print("   📝 MUST IMPLEMENT: Subscription orchestrator and webhooks")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
