#!/usr/bin/env python3

# Test script to run validation
import sys
import os
sys.path.append('/home/andre/projects/jtp-biological-organism')

try:
    from infrastructure.comprehensive_validation_audit import ComprehensiveValidationAudit

    audit = ComprehensiveValidationAudit()
    results = audit.validate_progress_tracking_data_flow()

    print("Progress Tracking Data Flow Validation Results:")
    print("=" * 50)
    print(f"Status: {results['status']}")
    print(f"Data Flow Score: {results['data_flow_score']}")
    print(f"Issues Found: {len(results['issues_found'])}")

    for issue in results['issues_found'][:5]:  # Show first 5
        print(f"  - {issue}")

    print("\nData Flow Connectivity:")
    for key, value in results['data_flow_connectivity'].items():
        status = "✅" if value else "❌"
        print(f"  {status} {key}: {value}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
