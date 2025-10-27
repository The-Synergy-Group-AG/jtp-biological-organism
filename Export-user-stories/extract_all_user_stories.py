#!/usr/bin/env python3
"""
Extract all user stories from the entire codebase.
"""

import os
import re
import pandas as pd
from typing import Dict

def extract_all_user_stories() -> Dict[str, Dict[str, str]]:
    """Extract all user stories from all sources"""
    user_stories = {}

    # Search in multiple directories and files
    search_paths = [
        'docs/9.x-user-interface/9.1-wireframes',
        'implementation-code/modules',
        'testing-code',
        'docs',
        '.'
    ]

    # Patterns to find user stories
    patterns = [
        r'US-(\d+):?\s*([^"\n]+?)(?:\s*→\s*|\s*-\s*)"([^"]+)"',
        r'US-(\d+)[:\s]+([^-"\n]+?)\s*[-–]\s*"([^"]+)"',
        r'US-(\d+)[:\s]+([^\n]+)',
        r'(?:\*\*)?US-(\d+)(?:\*\*)?[:\s]+([^\n]+)',
    ]

    for base_path in search_paths:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.md') or file.endswith('.txt'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()

                            # Try each pattern
                            for pattern in patterns:
                                matches = re.findall(pattern, content, re.MULTILINE)
                                for match in matches:
                                    if len(match) >= 2:
                                        try:
                                            if len(match) >= 3:
                                                story_id = f'US-{match[0]}'
                                                title = match[1].strip()
                                                description = match[2].strip().strip('"')
                                            else:
                                                story_id = f'US-{match[0]}'
                                                title_desc = match[1].strip()
                                                if ':' in title_desc:
                                                    parts = title_desc.split(':', 1)
                                                    title = parts[0].strip()
                                                    description = parts[1].strip().strip('"')
                                                else:
                                                    title = title_desc
                                                    description = ''

                                            # Clean up
                                            description = re.sub(r'^"|"$', '', description).strip()
                                            description = re.sub(r'^→\s*', '', description)

                                            if story_id not in user_stories and (title or description):
                                                user_stories[story_id] = {
                                                    'title': title,
                                                    'description': description,
                                                    'source_file': filepath.replace('/home/andre/projects/jtp-ai-first/', '')
                                                }
                                        except (IndexError, ValueError):
                                            continue
                        except Exception as e:
                            continue

    return user_stories

def format_comprehensive_output(stories: Dict[str, Dict[str, str]]) -> str:
    """Format all user stories for output"""
    output = []
    output.append('# Complete User Story Collection (456 Stories)')
    output.append('')
    output.append(f'Total unique user stories: {len(stories)}')
    output.append('')
    output.append('=' * 80)
    output.append('')

    # Sort by story ID
    sorted_ids = sorted(stories.keys(), key=lambda x: int(x.split('-')[1]))

    for story_id in sorted_ids:
        story = stories[story_id]
        output.append(f'{story_id} | {story["title"]} | "{story["description"]}"')
        output.append(f'   Source: {story["source_file"]}')
        output.append('')

    return '\n'.join(output)

if __name__ == "__main__":
    # Extract all stories
    all_stories = extract_all_user_stories()

    # Format output
    formatted_output = format_comprehensive_output(all_stories)

    # Save to file
    with open('/home/andre/projects/jtp-ai-first/user_stories_complete_456.txt', 'w', encoding='utf-8') as f:
        f.write(formatted_output)

    # Save as CSV
    csv_data = []
    sorted_ids = sorted(all_stories.keys(), key=lambda x: int(x.split('-')[1]))
    for story_id in sorted_ids:
        story = all_stories[story_id]
        csv_data.append([story_id, story['title'], story['description'], story['source_file']])

    df = pd.DataFrame(csv_data, columns=['Story ID', 'Title', 'Description', 'Source File'])
    df.to_csv('/home/andre/projects/jtp-ai-first/user_stories_complete_456.csv', index=False)

    print(f'Successfully extracted {len(all_stories)} user stories!')
    print('Saved to:')
    print('- user_stories_complete_456.txt')
    print('- user_stories_complete_456.csv')
    print('')
    print('Sample of first 10 stories:')
    # Show sample
    sorted_ids = sorted(all_stories.keys(), key=lambda x: int(x.split('-')[1]))
    for i, story_id in enumerate(sorted_ids[:10]):
        story = all_stories[story_id]
        print(f'{story_id}: {story["title"]}')
