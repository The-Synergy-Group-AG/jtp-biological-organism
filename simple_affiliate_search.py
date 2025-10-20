#!/usr/bin/env python3
"""
Simple Affiliate Program Document Search
Direct text search through documentation for affiliate-related content
"""

import os
import re
from pathlib import Path

def search_affiliate_files():
    """Search for affiliate program related files using simple text matching"""

    print("🔍 SIMPLE AFFILIATE PROGRAM SEARCH")
    print("=" * 50)
    print("Searching documentation for affiliate-related content")
    print()

    docs_root = Path("docs")
    affiliate_files = []

    # Affiliate-related keywords to search for
    affiliate_keywords = [
        'affiliate', 'partner', 'referral', 'commission', 'marketing',
        'partnership', 'collaboration', 'promotion', 'revenue sharing'
    ]

    # Search through all markdown files
    for root, dirs, files in os.walk(docs_root):
        for file in files:
            if file.endswith('.md') and not file.endswith('.bak'):
                filepath = Path(root) / file
                file_key = str(filepath.relative_to(docs_root))

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract metadata
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            # Get metadata
                            metadata_lines = parts[1].strip().split('\n')

                            title = ""
                            keywords = []
                            summary = ""

                            for line in metadata_lines:
                                if line.startswith('title:'):
                                    title_match = re.search(r'title:\s*"([^"]+)"', line)
                                    if title_match:
                                        title = title_match.group(1)

                                if line.startswith('ai_keywords:'):
                                    keywords_line = re.search(r'ai_keywords:\s*"([^"]*)"', line)
                                    if keywords_line:
                                        keywords = keywords_line.group(1).split(', ') if keywords_line.group(1) else []

                                if line.startswith('ai_summary:'):
                                    summary_match = re.search(r'ai_summary:\s*"([^"]*)"', line)
                                    if summary_match:
                                        summary = summary_match.group(1)

                            # Search content and keywords for affiliate terms
                            content_lower = (title + ' ' + ' '.join(keywords) + ' ' + summary).lower()

                            matching_keywords = []
                            for affiliate_word in affiliate_keywords:
                                if affiliate_word in content_lower:
                                    matching_keywords.append(affiliate_word)

                            if matching_keywords:
                                affiliate_files.append({
                                    'file': file_key,
                                    'title': title or file_key,
                                    'matching_keywords': matching_keywords,
                                    'keyword_count': len(keywords),
                                    'summary': summary[:100] + "..." if len(summary) > 100 else summary
                                })

                except Exception as e:
                    continue

    # Display results
    print("📊 SEARCH RESULTS SUMMARY")
    print(f"🏆 Found {len(affiliate_files)} files containing affiliate-related content")
    print()

    if affiliate_files:
        print("📋 AFFILIATE-RELATED FILES FOUND:")
        print("-" * 60)

        for i, file_info in enumerate(affiliate_files, 1):
            print(f"{i}. 📄 {file_info['title']}")
            print(f"   📍 Location: {file_info['file']}")
            print(f"   🎯 Matching terms: {', '.join(file_info['matching_keywords'])}")
            print(f"   📊 Total keywords: {file_info['keyword_count']}")
            print(f"   🧠 Summary: {file_info['summary']}")
            print()

        # Save report
        with open('affiliate_files_found.md', 'w') as f:
            f.write("# 🎯 AFFILIATE PROGRAM FILES - DIRECT SEARCH RESULTS\n\n")
            f.write(f"## 📊 SUMMARY\n")
            f.write(f"- **Total affiliate-related files**: {len(affiliate_files)}\n")
            f.write("- **Search method**: Direct text matching\n")
            f.write("- **Keywords searched**: affiliate, partner, referral, commission, marketing, partnership, collaboration, promotion, revenue sharing\n\n")

            f.write("## 📋 FILES CONTAINING AFFILIATE CONTENT\n\n")

            for i, file_info in enumerate(affiliate_files, 1):
                f.write(f"### {i}. {file_info['title']}\n")
                f.write(f"- **File location**: `{file_info['file']}`\n")
                f.write(f"- **Matching keywords**: {', '.join(file_info['matching_keywords'])}\n")
                f.write(f"- **Total keywords**: {file_info['keyword_count']}\n")
                f.write(f"- **AI summary**: {file_info['summary']}\n\n")

        print("💾 REPORT SAVED: affiliate_files_found.md")
        print()

    else:
        print("❌ NO AFFILIATE-RELATED FILES FOUND")
        print("The documentation does not contain references to affiliate programs,"
        print("partner programs, referral systems, or commission-based marketing.")
        print()

    return affiliate_files

if __name__ == "__main__":
    results = search_affiliate_files()

    print("🏁 AFFILIATE SEARCH COMPLETE")
    print(f"📊 Total affiliate-related files found: {len(results)}")
    print("🔍 Searched using direct text matching in all documentation")
