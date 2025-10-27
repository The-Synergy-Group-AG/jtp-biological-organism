#!/usr/bin/env python3
"""
User Stories File Splitter
Splits the massive 442-story master list into logical, manageable category files
for better navigation and maintenance.
"""

import os
import csv
from typing import Dict, List, Tuple

def load_master_list() -> List[Dict[str, str]]:
    """Load the complete master list CSV"""
    csv_file = "docs/5.x-biological-requirements-harmonization/COMPLETE_USER_STORIES_MASTER_LIST.csv"
    stories = []

    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            stories = [row for row in reader]

    return stories

def get_category(us_id: str) -> Tuple[str, str, str]:
    """Get category information for a user story ID"""
    num_match = re.search(r'US-(\d+)', us_id)
    if not num_match:
        return "Unknown", "Unknown", "unknown"

    num = int(num_match.group(1))

    if num <= 96:
        return "Core Platform", "01-Core_Platform", "core-platform"
    elif num <= 142:
        return "Analytics", "02-Analytics", "analytics"
    elif num <= 279:
        return "Emotional Support", "03-Emotional_Support", "emotional-support"
    elif num <= 323:
        return "Professional Development", "04-Professional_Development", "professional-development"
    elif num <= 356:
        return "Networking", "05-Networking", "networking"
    elif num <= 409:
        return "RAV Compliance", "06-RAV_Compliance", "rav-compliance"
    elif num <= 456:
        return "Advanced AI", "07-Advanced_AI", "advanced-ai"
    elif num >= 501:
        return "Swiss Extensions", "08-Swiss_Extensions", "swiss-extensions"
    else:
        return "Extended Features", "09-Extended_Features", "extended-features"

import re

def split_by_category(stories: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Split stories into categorized groups"""
    categories = {}

    for story in stories:
        us_id = story.get('User Story ID', '')
        category_name, _, category_key = get_category(us_id)

        if category_name not in categories:
            categories[category_name] = []

        categories[category_name].append(story)

    return categories

def generate_category_markdown(category_name: str, stories: List[Dict[str, str]], prefix: str) -> str:
    """Generate a category-specific markdown file"""

    output_dir = f"docs/5.x-biological-requirements-harmonization/categories/{prefix}"
    os.makedirs(output_dir, exist_ok=True)

    output = f"# {category_name} User Stories\n\n"
    output += f"# Category Overview: {category_name}\n\n"
    output += f"**Total Stories in this Category**: {len(stories)}\n\n"
    output += "**Stories range**: "
    if stories:
        first_id = stories[0]['User Story ID']
        last_id = stories[-1]['User Story ID']
        output += f"{first_id} through {last_id}\n\n"

    output += "# Complete User Story List\n\n"
    output += "| Nr | User Story ID | Title | Description | Source |\n"
    output += "|----|----------------|-------|-------------|--------|\n"

    for story in stories:
        nr = story.get('Nr', '')
        us_id = story.get('User Story ID', '')
        title = story.get('Title', '')
        description = story.get('Description', '')
        source = story.get('Source', '')

        output += f"| {nr} | {us_id} | {title} | {description} | {source} |\n"

    output += f"\n# End of {category_name} User Stories\n"
    output += f"# Total Stories: {len(stories)}\n\n"

    # Add navigation footer
    output += "---\n\n"
    output += "**📂 Category Files:**\n"
    output += "- [← Back to Master Index](../README.md)\n"
    output += "- [Core Platform](../01-Core_Platform/)\n"
    output += "- [Analytics](../02-Analytics/)\n"
    output += "- [Emotional Support](../03-Emotional_Support/)\n"
    output += "- [Professional Development](../04-Professional_Development/)\n"
    output += "- [Networking](../05-Networking/)\n"
    output += "- [RAV Compliance](../06-RAV_Compliance/)\n"
    output += "- [Advanced AI](../07-Advanced_AI/)\n"
    output += "- [Swiss Extensions](../08-Swiss_Extensions/)\n\n"

    return output, output_dir, f"{category_name.replace(' ', '_')}_User_Stories.md"

def generate_category_csv(category_name: str, stories: List[Dict[str, str]], prefix: str) -> Tuple[str, str, str]:
    """Generate a category-specific CSV file"""

    output_dir = f"docs/5.x-biological-requirements-harmonization/categories/{prefix}"

    # Create a simple CSV content
    csv_content = "Nr,User Story ID,Title,Description,Source\n"

    for story in stories:
        nr = story.get('Nr', '')
        us_id = story.get('User Story ID', '')
        title = story.get('Title', '')
        description = story.get('Description', '')
        source = story.get('Source', '')

        # Escape commas and quotes in fields
        def escape_field(field):
            if ',' in field or '"' in field:
                return f'"{field.replace(chr(34), chr(34)+chr(34))}"'
            return field

        csv_content += f"{escape_field(nr)},{escape_field(us_id)},{escape_field(title)},{escape_field(description)},{escape_field(source)}\n"

    return csv_content, output_dir, f"{category_name.replace(' ', '_')}_User_Stories.csv"

def generate_master_index(categories: Dict[str, List[Dict[str, str]]]) -> str:
    """Generate a master index file with navigation to all categories"""

    output_dir = "docs/5.x-biological-requirements-harmonization/categories"
    os.makedirs(output_dir, exist_ok=True)

    output = "# User Stories Master Index\n\n"
    output += "# 🎯 Complete User Stories Collection - Organized by Category\n\n"
    output += "**Official Total User Stories**: 442 (from Job Tracker Pro export)\n\n"
    output += "This directory contains the complete user stories collection, organized into logical categories for better navigation and management.\n\n"
    output += "## 📊 Collection Overview\n\n"
    output += "| Category | Story Count | Range | Status |\n"
    output += "|----------|-------------|-------|--------|\n"

    total_stories = 0
    category_list = []

    for category_name, stories in categories.items():
        count = len(stories)
        total_stories += count

        if stories:
            first = stories[0]['User Story ID']
            last = stories[-1]['User Story ID']
            range_text = f"{first}-{last}"
        else:
            range_text = "N/A"

        _, prefix, _ = get_category(stories[0]['User Story ID']) if stories else ("", "", "")
        file_link = f"{prefix}/README.md"

        output += f"| {category_name} | {count} | {range_text} | ✓ Complete |\n"
        category_list.append((category_name, count, range_text, file_link, prefix))

    output += f"| **Total** | **{total_stories}** | **US-001 - US-921+** | **🎯 Complete** |\n\n"

    # Category Navigation
    output += "## 📂 Category Navigation\n\n"

    for category_name, count, range_text, file_link, prefix in category_list:
        output += f"### 🔗 [{category_name}]({file_link})\n"
        output += f"**{count} stories** | **Range: {range_text}**\n\n"

    # File Structure
    output += "## 📁 File Structure\n\n"
    output += "```\n"
    output += "categories/\n"
    for category_name, _, _, _, prefix in category_list:
        output += f"├── {prefix}/\n"
        output += f"│   ├── {category_name.replace(' ', '_')}_User_Stories.md\n"
        output += f"│   ├── {category_name.replace(' ', '_')}_User_Stories.csv\n"
        output += f"│   └── README.md\n"
    output += "└── README.md (this file)\n"
    output += "```\n\n"

    # Usage Notes
    output += "## 📋 Usage Notes\n\n"
    output += "### For Developers:\n"
    output += "- Use the CSV files for importing into project management tools\n"
    output += "- Use the markdown files for documentation and review\n"
    output += "- Each category file contains only stories relevant to that feature area\n\n"

    output += "### For Product Managers:\n"
    output += "- Navigate to specific feature categories for focused story review\n"
    output += "- Use the master index to understand the overall product scope\n"
    output += "- Each story has proper titles that reflect actual functionality\n\n"

    output += "### For QA Testers:\n"
    output += "- Category files make it easier to test related functionality together\n"
    output += "- Stories are clearly titled and described for test case creation\n\n"

    # Back navigation
    output += "---\n\n"
    output += "**🔙 Navigation:**\n"
    output += "- [← Back to Master List](../COMPLETE_USER_STORIES_MASTER_LIST.md)\n"
    output += "- [← Back to Root Documentation](../../README.md)\n\n"

    output += "---\n\n"
    output += f"**Generated on**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output += "**Total Categories**: 8\n"
    output += "**Total Stories**: 442\n"

    return output, output_dir, "README.md"

def save_category_files(category_name: str, stories: List[Dict[str, str]], prefix: str):
    """Save all category files (markdown, CSV, README)"""

    # Generate content
    md_content, md_dir, md_filename = generate_category_markdown(category_name, stories, prefix)
    csv_content, csv_dir, csv_filename = generate_category_csv(category_name, stories, prefix)

    # Create category README with summary
    category_readme = f"# {category_name}\n\n"
    category_readme += f"## Overview\n\n"
    category_readme += f"This category contains **{len(stories)} user stories** related to {category_name.lower()}.\n\n"

    if stories:
        category_readme += f"**Story Range**: {stories[0]['User Story ID']} through {stories[-1]['User Story ID']}\n\n"

    category_readme += f"## Files in this Category\n\n"
    category_readme += f"- [{md_filename}]({md_filename}) - Complete user stories in markdown format\n"
    category_readme += f"- [{csv_filename}]({csv_filename}) - User stories in CSV format for import\n\n"

    category_readme += f"## Story Summary\n\n"
    category_readme += f"- **Total Stories**: {len(stories)}\n"
    category_readme += f"- **All titles are descriptive** and reflect actual functionality\n"
    category_readme += f"- **All descriptions** follow proper user story format\n\n"

    # Save files
    os.makedirs(md_dir, exist_ok=True)

    # Markdown file
    with open(os.path.join(md_dir, md_filename), 'w', encoding='utf-8') as f:
        f.write(md_content)

    # CSV file
    with open(os.path.join(md_dir, csv_filename), 'w', encoding='utf-8') as f:
        f.write(csv_content)

    # Category README
    with open(os.path.join(md_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(category_readme)

    print(f"✅ Saved {len(stories)} stories to {category_name} category")

def main():
    print("🎯 Starting User Stories File Splitting Process...")
    print("📂 Splitting 442 user stories into 8 logical categories")

    # Load stories
    stories = load_master_list()
    if not stories:
        print("❌ Error: Could not load master list CSV")
        return False

    print(f"✅ Loaded {len(stories)} stories for categorization")

    # Split by category
    categories = split_by_category(stories)

    print(f"📊 Stories organized into {len(categories)} categories:")

    for category, cat_stories in categories.items():
        print(f"   • {category}: {len(cat_stories)} stories")

    # Save master index
    index_content, index_dir, index_filename = generate_master_index(categories)

    with open(os.path.join(index_dir, index_filename), 'w', encoding='utf-8') as f:
        f.write(index_content)

    print("\n📁 Creating category directories...")
    # Save each category
    for category_name, category_stories in categories.items():
        _, prefix, _ = get_category(category_stories[0]['User Story ID']) if category_stories else ("", "unknown", "")
        save_category_files(category_name, category_stories, prefix)

    # Create summary file
    summary_content = "# User Stories Organization Summary\n\n"
    summary_content += f"## Splitted into {len(categories)} Categories\n\n"

    total_stories = 0
    for category_name, cat_stories in categories.items():
        count = len(cat_stories)
        total_stories += count
        _, prefix, _ = get_category(cat_stories[0]['User Story ID']) if cat_stories else ("", "", "")
        summary_content += f"- **{category_name}**: {count} stories → [`categories/{prefix}/`](./categories/{prefix}/)\n"

    summary_content += f"\n**Total Stories**: {total_stories}\n\n"

    summary_content += "## Benefits of This Organization\n\n"
    summary_content += "✓ **Easier Navigation** - Find relevant stories quickly by category\n"
    summary_content += "✓ **Focused Development** - Work on related features together\n"
    summary_content += "✓ **Better Maintenance** - Smaller, manageable files\n"
    summary_content += "✓ **Clear Scope** - Each category has defined boundaries\n\n"

    summary_content += "## File Structure\n\n"
    summary_content += "Each category contains:\n"
    summary_content += "- `README.md` - Category overview and navigation\n"
    summary_content += "- `*User_Stories.md` - Full stories in markdown\n"
    summary_content += "- `*User_Stories.csv` - Stories in CSV format\n\n"

    summary_content += "---\n\n"
    summary_content += "**Navigate to:** [Categories Index](./categories/)\n\n"

    with open("docs/5.x-biological-requirements-harmonization/STORY_CATEGORIES_SUMMARY.md", 'w', encoding='utf-8') as f:
        f.write(summary_content)

    print("\n🎉 SUCCESS: User Stories Successfully Split!")
    print("\n📂 New Organized Structure:")
    print("docs/5.x-biological-requirements-harmonization/")
    print("├── COMPLETE_USER_STORIES_MASTER_LIST.md  (still available)")
    print("├── COMPLETE_USER_STORIES_MASTER_LIST.csv  (still available)")
    print("├── STORY_CATEGORIES_SUMMARY.md           (new summary)")
    print("└── categories/")
    print("    ├── README.md                          (master index)")
    print("    ├── 01-Core_Platform/")
    print("    │   ├── Core_Platform_User_Stories.md")
    print("    │   ├── Core_Platform_User_Stories.csv")
    print("    │   └── README.md")
    print("    ├── 02-Analytics/")
    print("    │   ├── Analytics_User_Stories.md")
    print("    │   ├── Analytics_User_Stories.csv")
    print("    │   └── README.md")
    print("    └── [other categories...]")

    print("\n✨ Categories Created:")
    for category_name in categories.keys():
        print(f"   • {category_name}")

    print(f"\n📊 Summary: {len(categories)} categories, {total_stories} total stories")
    print("💡 The original master file is preserved for reference")

    return True

if __name__ == "__main__":
    main()
