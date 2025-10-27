#!/usr/bin/env python3
"""
Definitively User Story List Creation Script
Creates a clean, consolidated master list of all user stories in the correct format
Based on ORIGINAL_369_USER_STORIES_MASTER_LIST_PART_A.md format
"""

import os
import re
import csv
from typing import List, Dict, Tuple

def parse_user_story_line(line: str) -> Tuple[str, str, str, str]:
    """
    Parse a user story line from the text export with flexible format handling.
    Returns: (id, title, description, source)
    """
    line = line.strip()

    # Extract user story ID first
    us_match = re.match(r'^(US-\d+)\s', line)
    if not us_match:
        return "", "", "", ""

    user_story_id = us_match.group(1)

    # Remove the US-ID from the line for further processing
    remaining = line[len(user_story_id):].strip()

    # Extract source if present (usually at the end starting with "Source:")
    source = ""
    if '   Source: ' in remaining:
        parts = remaining.split('   Source: ', 1)
        remaining = parts[0].strip()
        source = parts[1].strip()

    # Handle different title/description patterns
    title = ""
    description = ""

    # Pattern 1: US-XXX | Title | "Description"
    if ' | ' in remaining:
        parts = remaining.split(' | ', 2)
        if len(parts) >= 2:
            title = parts[0].strip()
            if len(parts) > 1:
                description = parts[1].strip()
                if len(parts) > 2:
                    description += ' | ' + parts[2].strip()
    else:
        # Pattern 2: US-XXX | "Complete Description"
        remaining = remaining.strip('|').strip()
        if remaining.startswith('"') and remaining.endswith('"'):
            description = remaining[1:-1]
        elif remaining:
            description = remaining

    # Clean up the title
    title = clean_title(title)

    # Clean up the description
    description = clean_description(description)

    return user_story_id, title, description, source

def clean_title(title: str) -> str:
    """Clean up title format"""
    if not title:
        return ""

    # Remove specials characters and clean up
    title = title.strip()
    title = re.sub(r'[|]+', '', title)  # Remove extra pipes
    title = re.sub(r'[*]+', '', title)  # Remove asterisks
    title = re.sub(r'\s+', ' ', title)  # Normalize spaces

    # Remove malformed prefixes
    title = title.lstrip('@').lstrip('#').lstrip('-')

    return title

def clean_description(desc: str) -> str:
    """Clean up user story description format"""
    if not desc:
        return ""

    # Remove extra quotes and malformed content
    desc = desc.strip()
    if desc.startswith('"') and desc.endswith('"'):
        desc = desc[1:-1]
    elif desc.startswith('"'):
        desc = desc[1:]
    elif desc.endswith('"'):
        desc = desc[:-1]

    # Clean up special characters
    desc = re.sub(r'[|]+', ' ', desc)  # Replace pipes with spaces
    desc = re.sub(r'\s+', ' ', desc)  # Normalize spaces

    # Remove malformed content
    desc = desc.strip()

    return desc

def extract_user_story_from_complex_line(line: str) -> Tuple[str, str, str, str]:
    """
    Handle complex user story lines that don't follow simple patterns
    """
    line = line.strip()

    # Look for US-XXX pattern
    us_match = re.search(r'(US-\d+)', line)
    if not us_match:
        return "", "", "", ""

    user_story_id = us_match.group(1)

    # Extract everything after US-ID
    content = line[us_match.end():].strip()

    # Look for common patterns
    title = ""
    description = ""
    source = ""

    # Check for "As a" pattern (user story format)
    as_match = re.search(r'"As a[^"]*', content)
    if as_match:
        description = content[as_match.start():]
        # Everything before "As a" is title
        title = content[:as_match.start()].strip().rstrip('|').strip()
        if title.endswith('| ') or title.endswith(' |'):
            title = title[:-2].strip()
    else:
        # Fallback: first part title, rest description
        if '|' in content:
            parts = content.split('|', 1)
            title = parts[0].strip()
            if len(parts) > 1:
                description = parts[1].strip()
        else:
            description = content

    # Extract source if present
    source_pattern = r'\s+Source:\s+([^|]+?)$'
    source_match = re.search(source_pattern, line)
    if source_match:
        source = source_match.group(1).strip()
        # Remove source from description if it's there
        desc_source_pattern = r'Source:\s+' + re.escape(source)
        description = re.sub(desc_source_pattern, '', description).strip()

    # Clean up results
    title = clean_title(title)
    description = clean_description(description)

    return user_story_id, title, description, source

def clean_description(desc: str) -> str:
    """Clean up user story description format"""
    if not desc:
        return ""

    # Remove extra quotes and malformed content
    desc = desc.strip()
    if desc.startswith('"') and desc.endswith('"'):
        desc = desc[1:-1]

    # Clean up incomplete descriptions
    if desc.startswith('"') or desc.endswith('"'):
        desc = desc.strip('"')

    # Remove source information mixed in description
    if '   Source:' in desc:
        desc = desc.split('   Source:')[0].strip()

    return desc

def extract_all_user_stories() -> List[Tuple[str, str, str, str]]:
    """Extract and consolidate all user stories from the export files"""
    user_stories = []

    # Read from the main export file
    export_file = "Export-user-stories/user_stories_complete_456.txt"

    if os.path.exists(export_file):
        with open(export_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_entry_lines = []
        is_in_entry = False

        for line in lines:
            line = line.strip()

            # Skip headers and stats
            if line.startswith('#') or line.startswith('Total') or line.strip() == '':
                continue

            # Check if this starts a new entry
            if line.startswith('US-'):
                # Process previous entry if exists
                if current_entry_lines:
                    story = process_entry_lines(current_entry_lines)
                    if story[0]:  # Has user story ID
                        user_stories.append(story)
                    current_entry_lines = []

                # Start new entry
                current_entry_lines = [line]
                is_in_entry = True

            elif is_in_entry and (line.startswith('   Source:') or line.startswith('Source:')):
                # Add source line to current entry
                current_entry_lines.append(line)

        # Process final entry
        if current_entry_lines:
            story = process_entry_lines(current_entry_lines)
            if story[0]:
                user_stories.append(story)

    # Sort by US number
    def sort_key(story):
        id_str = story[0]
        if id_str.startswith('US-'):
            num_part = id_str[3:]
            try:
                return int(num_part)
            except ValueError:
                return 9999
        return 9999

    user_stories.sort(key=sort_key)
    return user_stories

def process_entry_lines(entry_lines: List[str]) -> Tuple[str, str, str, str]:
    """Process the lines for a single user story entry"""
    if not entry_lines:
        return "", "", "", ""

    main_line = ""
    source_line = ""

    for line in entry_lines:
        if line.startswith('US-'):
            main_line = line
        elif line.startswith('   Source:') or line.startswith('Source:'):
            source_line = line

    if not main_line:
        return "", "", "", ""

    # Parse the main user story line
    user_story_id, title, description, _ = parse_simple_user_story(main_line)

    # Extract source
    source = ""
    if source_line:
        source = source_line.replace('Source:', '').replace('   Source:', '').strip()

    # Clean up data
    title = clean_title(title)
    description = clean_description(description)

    return user_story_id, title, description, source

def parse_simple_user_story(line: str) -> Tuple[str, str, str, str]:
    """
    Simple, direct parsing of user story lines
    """
    line = line.strip()

    # Extract US-ID
    us_match = re.match(r'^(US-\d+)', line)
    if not us_match:
        return "", "", "", ""

    user_story_id = us_match.group(1)
    remaining = line[us_match.end():].strip()

    title = ""
    description = ""

    # Look for description in quotes
    quote_match = re.search(r'"([^"]*)"', remaining)
    if quote_match:
        description = quote_match.group(1).strip()
        # Everything before the quote is title
        title_part = remaining[:quote_match.start()].strip()
        # Clean up title part
        title_part = re.sub(r'[|]+\s*$', '', title_part)  # Remove trailing pipes
        title_part = re.sub(r'^\s*[|]+', '', title_part)  # Remove leading pipes
        title_part = re.sub(r'\*\*$', '', title_part)  # Remove trailing double asterisks
        title = title_part.strip()
    else:
        # No quotes - just use remaining as description
        description = remaining.strip()
        if ' | ' in description:
            # Split into title and description
            parts = description.split(' | ', 1)
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""

    return user_story_id, title, description, ""

def parse_complex_user_story(line: str) -> Tuple[str, str, str, str]:
    """
    Parse complex user story lines with multiple formats
    """
    line = line.strip()

    # Extract US-ID
    us_match = re.match(r'^(US-\d+)', line)
    if not us_match:
        return "", "", "", ""

    user_story_id = us_match.group(1)
    remaining = line[us_match.end():].strip()

    title = ""
    description = ""
    source = ""  # We'll extract this separately

    # Handle different patterns

    # Pattern 1: | Title | "Description" | Source: path
    if ' | ' in remaining and '"' in remaining:
        parts = re.split(r'\s*\|\s*', remaining)
        if len(parts) >= 3:
            # Remove empty parts
            parts = [p for p in parts if p.strip()]

            if len(parts) >= 1:
                title = parts[0].strip()
            if len(parts) >= 2 and '"' in parts[1]:
                desc_match = re.search(r'"([^"]*)"', parts[1])
                if desc_match:
                    description = desc_match.group(1)

    # Pattern 2: | | Title | metadata | "Description"
    elif remaining.startswith('| |'):
        parts = remaining.split('|')
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) >= 2:
            title = parts[1]
        if len(parts) >= 3 and '"' in parts[2]:
            desc_match = re.search(r'"([^"]*)"', parts[2])
            if desc_match:
                description = desc_match.group(1)

    # Pattern 3: Title | "Description"
    elif '"' in remaining:
        quote_match = re.search(r'"([^"]*)"', remaining)
        if quote_match:
            description = quote_match.group(1)
            title_part = remaining[:quote_match.start()].strip()
            if ' | ' in title_part:
                title = title_part.split(' | ')[0].strip()
            else:
                title = title_part

    # Pattern 4: | Title | Description
    elif ' | ' in remaining and not '"' in remaining:
        parts = [p.strip() for p in remaining.split('|') if p.strip()]
        if len(parts) >= 1:
            title = parts[0]
        if len(parts) >= 2:
            description = parts[1]

    # Pattern 5: Just description without quotes
    elif remaining and not remaining.startswith('|'):
        if not remaining.startswith('*') and 'to US-' not in remaining:
            # Check if it looks like a description
            if len(remaining) > 10 and not remaining.startswith('('):
                description = remaining

    return user_story_id, title, description, source

def create_master_list(user_stories: List[Tuple[str, str, str, str]]) -> str:
    """Create the master list in the format of ORIGINAL_369_USER_STORIES_MASTER_LIST_PART_A.md"""
    output = "# Original 369 User Stories Master List - Complete Collection\n\n"
    output += "# SUMMARY TABLE: Complete User Stories by Source System\n"
    output += "| Source System | Number of User Stories |\n"
    output += "|---------------|-----------------------|\n"
    output += "| Exported from Job Tracker Pro | 442 |\n"
    output += "| **Complete Collection** | **442** |\n\n"

    output += "# COMPREHENSIVE USER STORY DATABASE - DEFINITIVE MANIFEST\n"
    output += "OFFICIAL TOTAL USER STORIES: 442 (from Job Tracker Pro export)\n"
    output += "This file contains the complete collection of user stories extracted and cleaned\n"
    output += "Format: Sequential numbering with User Story ID, Title, Description, and Source\n"
    output += "\n+++++\n\n"

    output += "| Nr | User Story ID | Title | Description | Source |\n"
    output += "|----|----------------|-------|-------------|--------|\n"

    for i, (us_id, title, description, source) in enumerate(user_stories, 1):
        # Format the row properly
        title_clean = title[:50] + "..." if len(title) > 50 else title
        desc_clean = description[:80] + "..." if len(description) > 80 else description

        output += f"| {i} | {us_id} | {title_clean} | {desc_clean} | {source} |\n"

    output += "\n# End of Complete User Stories Collection\n"
    output += f"# Total User Stories: {len(user_stories)}\n"
    output += "# Generated from Export-user-stories folder\n"

    return output

def create_csv_version(user_stories: List[Tuple[str, str, str, str]]) -> None:
    """Create a CSV version for import into other tools"""
    csv_filename = "docs/5.x-biological-requirements-harmonization/COMPLETE_USER_STORIES_MASTER_LIST.csv"

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Nr', 'User Story ID', 'Title', 'Description', 'Source'])

        for i, (us_id, title, description, source) in enumerate(user_stories, 1):
            writer.writerow([i, us_id, title, description, source])

    print(f"CSV file created: {csv_filename}")

def main():
    print("🚀 Starting definitive user story list creation...")

    # Extract all user stories
    user_stories = extract_all_user_stories()
    print(f"📊 Extracted {len(user_stories)} user stories")

    # Create the master list
    master_content = create_master_list(user_stories)

    # Save to the target location
    target_file = "docs/5.x-biological-requirements-harmonization/COMPLETE_USER_STORIES_MASTER_LIST.md"
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(master_content)

    print(f"✅ Master list saved to: {target_file}")

    # Create CSV version
    create_csv_version(user_stories)
    print("✅ CSV version created")

    # Summary statistics
    print(".2e")
    print(f"🔍 Stories with descriptions: {len([us for us in user_stories if us[2]])}")
    print(f"📝 Stories with titles: {len([us for us in user_stories if us[1]])}")

    print("\n🎉 Definitive user stories master list creation complete!")

    # Show first few entries as example
    print("\n📋 First 5 entries:")
    for i, story in enumerate(user_stories[:5], 1):
        us_id, title, desc, source = story
        print(".50")

if __name__ == "__main__":
    main()
