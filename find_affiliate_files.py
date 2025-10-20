#!/usr/bin/env python3
"""
🔍 AFFILIATE PROGRAM FILE DISCOVERY
Using the GODHOOD biological AI search system to find all files related to affiliate programs
Demonstrates the power of our 6-tier biological intelligence system
"""

import sys
import os
sys.path.append('.')
from biological_ai_enhancement_system import BiologicalAIEnhancementSystem

def find_affiliate_program_files():
    """Find all files related to affiliate programs using GODHOOD AI search"""

    print("🎯 AFFILIATE PROGRAM FILE DISCOVERY")
    print("=" * 60)
    print("Using GODHOOD Biological AI Intelligence to find affiliate-related content")
    print()

    # Search queries for affiliate programs
    affiliate_queries = [
        "affiliate program",
        "affiliate marketing",
        "partner program",
        "referral program",
        "affiliate system",
        "commission program",
        "partner marketing",
        "affiliate management"
    ]

    all_results = []

    for i, query in enumerate(affiliate_queries, 1):
        print(f"🔍 Searching with query #{i}: '{query}'")
        print("-" * 40)

        # Use our GODHOOD enhanced search
        system = BiologicalAIEnhancementSystem()
        system.load_document_intelligence()
        system.enhance_with_vector_intelligence()
        system.enhance_with_relationship_mining()
        system.enhance_with_intent_analysis()
        system.enhance_with_evolutionary_phase_intelligence()
        system.enhance_with_biological_metaphor_recognition()
        system.enhance_with_temporal_freshness_scoring()

        results = system.godhood_biological_search_enhanced(query, limit=10)

        print(f"📊 Found {len(results)} relevant files")

        for result in results:
            if result['score'] > 20:  # Filter for reasonably relevant results
                # Avoid duplicates
                if not any(r['doc_id'] == result['doc_id'] for r in all_results):
                    result['search_query'] = query
                    all_results.append(result)
                    print(".1f"
                    print(f"   📁 {result['doc_id']}")
                    print(f"   📚 {result['title']}")
                    print(f"   🏗️ Phase: {result['phase']}")
                    print(f"   🧬 Biology: {result['biological_system']}")
                    print()

    # Deduplicate and rank by score
    unique_results = []
    seen_files = set()

    for result in sorted(all_results, key=lambda x: x['score'], reverse=True):
        if result['doc_id'] not in seen_files:
            seen_files.add(result['doc_id'])
            unique_results.append(result)

    # Create comprehensive report
    print("📈 COMPREHENSIVE AFFILIATE PROGRAM FILE REPORT")
    print("=" * 60)
    print(f"🎯 Total Unique Affiliate-Related Files Found: {len(unique_results)}")
    print("🧬 Discovered through GODHOOD Biological AI Intelligence")
    print()

    if unique_results:
        print("🏆 TOP AFFILIATE-RELATED FILES BY RELEVANCE:")
        print("-" * 50)

        for i, result in enumerate(unique_results[:20], 1):  # Show top 20
            print(f"{i}. 📄 {result['title']}")
            print(".1f"            print(f"   📍 Location: {result['doc_id']}")
            print(f"   🔍 Found via: {result['search_query']}")
            print(f"   🏗️ Evolutionary Phase: {result['phase']}")
            print(f"   🧬 Biological System: {result['biological_system']}")
            print(f"   📊 Relevance Keywords: {len(result['matching_keywords'])} matches")
            if result['matching_keywords']:
                print(f"   🎯 Matching Terms: {', '.join(result['matching_keywords'])}")
            print(f"   🧠 AI Summary: {result['ai_summary']}")
            print()

        # Save to file
        with open('affiliate_program_files_report.md', 'w') as f:
            f.write("# 🎯 AFFILIATE PROGRAM FILES DISCOVERY REPORT\n\n")
            f.write("## 📊 EXECUTIVE SUMMARY\n")
            f.write(f"- **Total Files Discovered**: {len(unique_results)}\n")
            f.write("- **Search Method**: GODHOOD Biological AI Intelligence\n")
            f.write("- **Queries Used**: 8 affiliate-related search terms\n")
            f.write("- **Discovery Engine**: 6-tier biological enhancement system\n\n")

            f.write("## 📋 COMPLETE FILE LIST\n\n")

            for i, result in enumerate(unique_results, 1):
                f.write(f"### {i}. {result['title']}\n")
                f.write(".1f"                f.write(f"- **Location**: `{result['doc_id']}`\n")
                f.write(f"- **Phase**: {result['phase']}\n")
                f.write(f"- **Biological System**: {result['biological_system']}\n")
                f.write(f"- **Found via query**: '{result['search_query']}'\n")
                if result['matching_keywords']:
                    f.write(f"- **Matching keywords**: {', '.join(result['matching_keywords'])}\n")
                f.write(f"- **Summary**: {result['ai_summary']}\n\n")

        print("💾 REPORT SAVED: affiliate_program_files_report.md")
        print("🎯 Found all affiliate program related files using biological AI intelligence!")

    else:
        print("❌ No affiliate program files found in the documentation")
        print("💡 The GODHOOD AI search system found zero matches for affiliate-related content")

    return unique_results

if __name__ == "__main__":
    results = find_affiliate_program_files()

    print("
🏁 AFFILIATE PROGRAM DISCOVERY COMPLETE"    print(f"📊 Total affiliate-related files identified: {len(results)}")
    print("🧬 Discovered through GODHOOD biological AI intelligence"
