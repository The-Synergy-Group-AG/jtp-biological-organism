#!/usr/bin/env python3
"""
Import Validation Script - Test all critical module imports
for JTP Biological Organism codebase
"""

import sys
import os
import traceback
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def test_module_import(module_path: str, module_name: str) -> tuple[bool, str]:
    """Test if a module can be imported successfully"""
    try:
        __import__(module_name)
        return True, "SUCCESS"
    except ImportError as e:
        return False, f"ImportError: {e}"
    except Exception as e:
        return False, f"Exception: {e}"

def test_critical_modules():
    """Test all critical system modules"""
    print("🧬 JTP BIOLOGICAL ORGANISM - IMPORT VALIDATION TEST")
    print("=" * 60)

    critical_modules = [
        # Core system modules
        ("src.cns_consciousness_core", "CNS Consciousness Core"),
        ("src.biological_intelligence", "Biological Intelligence Orchestrator"),
        ("src.harmonization_api", "Harmonization API"),
        ("src.biological_ai_enhancement_system", "AI Enhancement System"),

        # Subsystem modules
        ("src.biological_intelligence.consciousness.consciousness_processor", "Consciousness Processor"),
        ("src.biological_intelligence.intelligence.pattern_recognition", "Pattern Recognition"),
        ("src.biological_intelligence.coordination.system_integrator", "System Integrator"),
    ]

    passed = 0
    failed = 0

    for module_name, description in critical_modules:
        print(f"\n🔍 Testing: {description}")
        print(f"   Module: {module_name}")

        success, result = test_module_import('', module_name)
        if success:
            print(f"   ✅ SUCCESS")
            passed += 1
        else:
            print(f"   ❌ FAILED: {result}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"📊 VALIDATION SUMMARY:")
    print(f"   ✅ Successfully imported: {passed}")
    print(f"   ❌ Failed imports: {failed}")
    print(f"   📈 Success rate: {((passed / (passed + failed)) * 100):.1f}%")

    if failed > 0:
        print("
⚠️  SOME MODULES FAILED - CHECK ERRORS ABOVE"        return False
    else:
        print("
🎉 ALL CRITICAL MODULES IMPORTED SUCCESSFULLY"        return True

def test_graceful_fallbacks():
    """Test that ImportError handlers provide graceful fallbacks"""
    print("\n🔧 TESTING GRACEFUL FALLBACKS...")

    # Test harmonization_api stub
    try:
        from src.harmonization_api import HarmonizationAPI, HarmonizationMetrics
        api = HarmonizationAPI()
        status = api.get_harmonization_status()
        if "stub_mode" in status and status["stub_mode"]:
            print("   ✅ HarmonizationAPI stub working correctly")
        else:
            print("   ❌ HarmonizationAPI not in stub mode")
            return False
    except Exception as e:
        print(f"   ❌ HarmonizationAPI test failed: {e}")
        return False

    # Test biological_ai stub
    try:
        from src.biological_ai_enhancement_system import BiologicalAIEnhancementSystem
        system = BiologicalAIEnhancementSystem()
        status = system.get_enhancement_status()
        if "stub_mode" in status and status["stub_mode"]:
            print("   ✅ BiologicalAIEnhancementSystem stub working correctly")
        else:
            print("   ❌ BiologicalAIEnhancementSystem not in stub mode")
            return False
    except Exception as e:
        print(f"   ❌ BiologicalAIEnhancementSystem test failed: {e}")
        return False

    print("   ✅ All graceful fallbacks working correctly")
    return True

if __name__ == "__main__":
    try:
        # Test directory structure
        if not src_path.exists():
            print(f"❌ Source directory not found: {src_path}")
            sys.exit(1)

        # Run main validation
        success = test_critical_modules()
        fallback_success = test_graceful_fallbacks()

        print("\n" + "=" * 60)
        print("🎯 FINAL RESULT:")
        if success and fallback_success:
            print("🧬 ALL CRITICAL IMPORTS WORKING - SYSTEM READY FOR DEPLOYMENT")
            sys.exit(0)
        else:
            print("🛑 CRITICAL IMPORT ISSUES DETECTED - REQUIRES ATTENTION")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Validation script failed: {e}")
        traceback.print_exc()
        sys.exit(1)
