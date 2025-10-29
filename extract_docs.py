import os
import re
from pathlib import Path

def extract_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title_match = re.search(r'\*\*Document Title\*\* \| ([^\|]*)', content)
    ethical_match = re.search(r'\*\*Ethical Score\*\* \| ([^\|]*)', content)

    title = title_match.group(1).strip() if title_match else 'Unknown'
    ethical = ethical_match.group(1).strip() if ethical_match else 'No Score'

    return title, ethical

def main():
    docs_path = Path('docs')
    results = []

    for md_file in docs_path.rglob('*.md'):
        if md_file.name in ['README.md', 'biological_consciousness_system_documentation.md'] or md_file.suffix != '.md':
            continue  # skip root level or non-md

        folder = str(md_file.parent).replace('docs/', '').replace('docs', '') or 'Root'
        title, ethical = extract_metadata(md_file)
        results.append((folder, title, ethical))

    # Summary
    total = len(results)
    score_counts = {}
    for _, _, score in results:
        if '95%' in score:
            cat = '95%'
        elif '91%' in score:
            cat = '91%'
        elif '85%' in score:
            cat = '85%'
        else:
            cat = 'Other'
        score_counts[cat] = score_counts.get(cat, 0) + 1

    print('# Documentation Review Summary\n')
    print(f'**Total Documents Reviewed:** {total}\n')
    print('## Ethical Score Breakdown\n')
    for score, count in score_counts.items():
        print(f'- {score}: {count} documents')
    print()

    print('## Document Details\n')
    print('| Folder | Title | Ethical Score |')
    print('|--------|--------|---------------|')
    for folder, title, ethical in sorted(results, key=lambda x: (x[0], x[1])):
        print(f'| {folder} | {title} | {ethical} |')

    print('\n## Immediate Next Steps\n')
    print('1. **Review all 85% ⚠️ scored documents** - Conduct thorough ethical compliance audit and update as needed.')
    print('2. **Verify high-scoring documents** - Ensure 91% and 95% scores are accurate with peer review.')
    print('3. **Implement continuous monitoring** - Set up automated checks for new documentation to maintain standards.')
    print('4. **Training program** - Educate contributors on ethical score calculation and compliance requirements.')
    print('5. **Audit trail enhancement** - Improve versioning and change history documentation for ethical accountability.')

if __name__ == '__main__':
    main()
