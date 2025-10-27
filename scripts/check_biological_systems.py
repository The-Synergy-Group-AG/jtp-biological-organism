#!/usr/bin/env python3
"""
Check Biological Systems - Verify complete biological system inventory
"""

import os
import glob
import re

def find_all_biological_systems():
    """Find all mentioned biological systems across the framework"""

    print("🔍 Scanning biological framework for all systems...")

    systems_found = set()

    # Check all biological framework files
    framework_dir = "docs/5.x-biological-requirements-harmonization/biological-framework"

    if os.path.exists(framework_dir):
        for filename in os.listdir(framework_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(framework_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Look for biological system names using regex patterns
                    system_patterns = [
                        r'Biological System[:\s]*([^:\n]+)',
                        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Subconsciousness',
                        r'Subconsciousness\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                        r'([A-Z][a-z]+(?: [A-Z][a-z]+)+) Intelligence',
                        r'([A-Z][a-z]+)\s+Regulation',
                        r'([A-Z][a-z]+)\s+Integrity',
                        r'([A-Z][a-z]+)\s+Defense',
                        r'([A-Z][a-z]+)\s+Harmonization',
                    ]

                    for pattern in system_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Clean up the match
                            clean_match = match.strip()
                            if len(clean_match) > 3:  # Skip very short matches
                                systems_found.add(clean_match.title())

    # Check the biological integration database CSV
    csv_path = os.path.join(framework_dir, "E.1-biological-integration-mapping-database.csv")
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for biological systems in the CSV
            for line in content.split('\n'):
                if ',' in line and any(term in line.lower() for term in ['core', 'circulatory', 'muscular', 'respiratory', 'endocrine', 'skeletal', 'immune', 'energy', 'cooperation', 'multilingual']):
                    # This might be a mapping line, extract biological systems
                    parts = line.split(',')
                    if len(parts) >= 4:
                        bio_system = parts[3].strip().strip('"')
                        if bio_system and len(bio_system) > 3:
                            systems_found.add(bio_system.title())

    # Manual additions from file names
    manual_systems = [
        "CNS Consciousness Core",
        "Circulatory Resource Orchestration",
        "Muscular Execution Coordination",
        "Respiratory Intelligence Processing",
        "Endocrine Adaptation Regulation",
        "Skeletal Structural Integrity",
        "Immune Autonomous Defense",
        "Energy Field Harmonization",
        "Symbiotic Cooperation Frameworks",
        "Multilingual Resonance Adapter",
        "Digital Organism Interaction"
    ]

    systems_found.update(manual_systems)

    # Remove duplicates and sort
    unique_systems = sorted(list(set(systems_found)))
    unique_systems = [s for s in unique_systems if len(s) > 5 and s.upper() != s.lower()]  # Filter out noise

    print(f"📊 Found {len(unique_systems)} biological systems:")
    for i, system in enumerate(unique_systems, 1):
        print(f"   {i}. {system}")

    return unique_systems

def analyze_systems_coverage(biological_systems):
    """Analyze how well we cover biological systems with our current mapping"""

    print(f"\n🔍 Analyzing Coverage of {len(biological_systems)} Biological Systems:")

    current_mapping = {
        "CNS Consciousness Core": "Core Platform, Analytics",
        "Endocrine Adaptation Regulation": "Emotional Support",
        "Respiratory Intelligence Processing": "Professional Development",
        "Symbiotic Cooperation Frameworks": "Networking",
        "Skeletal Structural Integrity": "RAV Compliance",
        "Energy Field Harmonization": "Advanced AI",
        "Multilingual Resonance Adapter": "Swiss Extensions"
    }

    mapped_systems = set(current_mapping.keys())
    unmapped_systems = set(biological_systems) - mapped_systems

    print(f"✅ Mapped systems ({len(mapped_systems)}):")
    for system in mapped_systems:
        print(f"   • {system}: {current_mapping.get(system, 'No mapping')}")

    print(f"\n⚠️  Unmapped systems ({len(unmapped_systems)}):")
    for system in unmapped_systems:
        print(f"   • {system}")

    print(f"\n📈 Coverage: {len(mapped_systems)}/{len(biological_systems)} ({len(mapped_systems)/len(biological_systems)*100:.1f}% )")

    return unmapped_systems

def suggest_expanded_mapping(unmapped_systems):
    """Suggest how to incorporate unmapped biological systems"""

    if unmapped_systems:
        print(f"\n💡 Suggestions for incorporating {len(unmapped_systems)} unmapped systems:")

        suggestions = []
        for system in unmapped_systems:
            if "circulatory" in system.lower():
                suggestions.append(f"• {system}: Could be mapped to user story categories involving resource allocation and performance optimization")
            elif "muscular" in system.lower():
                suggestions.append(f"• {system}: Could enhance action-oriented stories with execution coordination capabilities")
            elif "immune" in system.lower():
                suggestions.append(f"• {system}: Could support security, compliance, and defensive features")
            elif "digital organism" in system.lower():
                suggestions.append(f"• {system}: Could enhance AI interaction and user-agent relationship stories")
            else:
                suggestions.append(f"• {system}: Could be integrated into platform foundation or cross-cutting concerns")

        for suggestion in suggestions:
            print(suggestion)

def main():
    """Main analysis function"""

    print("🧬 Analyzing Complete Biological Systems Inventory...\n")

    biological_systems = find_all_biological_systems()

    unmapped_systems = analyze_systems_coverage(biological_systems)

    suggest_expanded_mapping(unmapped_systems)

    print("\n🎯 Summary:")
    print(f"   Total Biological Systems: {len(biological_systems)}")
    print(f"   Currently Mapped: {len(biological_systems) - len(unmapped_systems)}")
    print(f"   Available for Integration: {len(unmapped_systems)}")

if __name__ == "__main__":
    main()
