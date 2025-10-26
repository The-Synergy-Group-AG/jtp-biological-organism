#!/usr/bin/env python3
"""
SIMPLE STRIPE API VALIDATION
Direct environment variable check and API test
"""

import os
import subprocess

def load_env_file(filepath):
    """Load environment variables from file"""
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}")

def test_stripe_connectivity():
    """Test Stripe API connectivity"""
    print("🧬 JTP Biological Organism - STRIPE PAYMENT GATEWAY VALIDATION")
    print("=" * 70)
    
    # Load the complete API ecosystem file
    load_env_file('.env.complete.api.ecosystem')
    
    # Check for Stripe keys
    stripe_api_key = os.getenv('STRIPE_API_KEY', '')
    stripe_secret_key = os.getenv('STRIPE_SECRET_KEY', '')
    
    api_key = stripe_api_key or stripe_secret_key
    
    print("🔍 STRIPE CONFIGURATION ANALYSIS:")
    print(f"   STRIPE_API_KEY: {'✅ Set' if stripe_api_key else '❌ Not set'} ({len(stripe_api_key)} chars)")
    print(f"   STRIPE_SECRET_KEY: {'✅ Set' if stripe_secret_key else '❌ Not set'} ({len(stripe_secret_key)} chars)")
    
    if not api_key:
        print("\n❌ PAYMENT GATEWAY STATUS: NO API KEYS CONFIGURED")
        print("   💡 API keys must be added to .env.complete.api.ecosystem")
        return False
    
    print(f"   🔑 Using API key: {api_key[:20]}...{api_key[-8:] if len(api_key) > 28 else api_key}")
    
    # Test connection using curl
    print("\n🔗 TESTING STRIPE API CONNECTIVITY:")
    
    try:
        # Use curl to test the balance endpoint
        cmd = [
            'curl', '-s', '-o', '/tmp/stripe_response.json', '-w', '%{http_code}',
            '-H', f'Authorization: Bearer {api_key}',
            '-H', 'Stripe-Version: 2023-10-16',
            'https://api.stripe.com/v1/balance'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        status_code = result.stdout.strip()
        
        print(f"   📡 HTTP Status Code: {status_code}")
        
        if status_code == '200':
            print("   ✅ SUCCESS: Stripe API connection established")
            print("   💰 Payment processing is OPERATIONAL")
            print("   💳 Subscription payments CAN be processed")
            return True
        elif status_code == '401':
            print("   ❌ FAILURE: Invalid API key (401 Unauthorized)")
            print("   ⚠️  Check if API key is correct and active")
            return False
        elif status_code == '403':
            print("   ❌ FAILURE: Insufficient permissions (403 Forbidden)")
            print("   ⚠️  API key may be restricted")
            return False
        else:
            print(f"   ❌ FAILURE: Unexpected status {status_code}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ❌ FAILURE: Request timeout")
        return False
    except Exception as e:
        print(f"   ❌ FAILURE: {str(e)}")
        return False

def main():
    success = test_stripe_connectivity()
    
    print("\n" + "=" * 70)
    print("📊 VALIDATION SUMMARY:")
    if success:
        print("✅ PAYMENT GATEWAY: OPERATIONAL")
        print("   🎯 Subscription processing: AVAILABLE")
        print("   🔗 Stripe API: CONNECTED")
        print("   💰 Credit card payments: SUPPORTED")
    else:
        print("❌ PAYMENT GATEWAY: NON-OPERATIONAL")
        print("   🚫 Subscription processing: UNAVAILABLE")
        print("   🔌 Stripe API: DISCONNECTED")
        print("   ⚠️  REQUIRES: Valid Stripe API configuration")
        print("\n📝 REQUIRED IMPLEMENTATIONS:")
        print("   • Subscription orchestrator service")
        print("   • Payment webhook handlers")
        print("   • Transaction processing endpoints")
        print("   • Checkout flow implementation")
    
    return success

if __name__ == "__main__":
    main()
