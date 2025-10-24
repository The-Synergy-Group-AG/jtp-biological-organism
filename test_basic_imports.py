#!/usr/bin/env python3
"""
🧬 Basic Import Test - GODHOOD Modular Components Verification
Tests fundamental imports without pytest complexity
Run: PYTHONPATH=/home/andre/projects/jtp-biological-organism/src python3 test_basic_imports.py
"""

import os
import sys

def test_imports():
    """Test basic module imports independently"""
    print("🧬 GODHOOD MODULAR IMPORT VERIFICATION")
    print("=" * 50)

    # Set Python path explicitly
    project_root = "/home/andre/projects/jtp-biological-organism"
    src_dir = os.path.join(project_root, "src")

    if not os.path.exists(src_dir):
        print(f"❌ Source directory not found: {src_dir}")
        return False

    # Add to Python path if not already there
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    # Test core personality matching imports
    import_tests = [
        ("personality_matching", "PersonalityProfile", "Core Personality"),
        ("personality_matching", "MultiDimensionalCompatibilityAnalyzer", "Compatibility Engine"),
        ("personality_matching", "ProfileAnalyzer", "Profile Analyzer"),
        ("personality_matching", "IntegrationFramework", "Integration Framework"),
        ("personality_matching", "PersonalityMatchingSystem", "Main Coordinator"),
        ("emotional_intelligence", "EmotionalProfileAnalyzer", "Emotional Intelligence"),
        ("emotional_intelligence", "EmpathyNetworkAnalyzer", "Empathy Network"),
    ]

    results = {}
    total_tests = len(import_tests)
    passed = 0

    for module_name, class_name, description in import_tests:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name, None)
            if cls:
                results[f"✅ {description}"] = f"Successfully imported {class_name}"
                passed += 1
            else:
                results[f"❌ {description}"] = f"Class {class_name} not found in module"
        except Exception as e:
            results[f"❌ {description}"] = f"Import failed: {e}"

    # Print results
    print(f"\n📊 IMPORT TEST RESULTS ({passed}/{total_tests} passed)")
    print("-" * 50)
    for item, result in results.items():
        print(f"{item}: {result}")

    print("-" * 50)
    if passed == total_tests:
        print("🎉 ALL MODULES IMPORTED SUCCESSFULLY!")
        print("🧬 MODULAR REFACTORING IS FUNCTIONAL")
        return True
    else:
        print(f"⚠️  {passed}/{total_tests} modules imported successfully")
        print("🔧 Environment configuration may still need adjustment")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
