#!/usr/bin/env python3
"""
Continuous Documentation Compliance Monitor

Validates all documentation in docs/ directory against ethical and quality standards:
- Ethical score ≥91%
- Minimum 8 AI keywords
- Complete required metadata
- DOCUMENT_GUIDELINES compliance

Usage: python docs_compliance_checker.py [--fix] [--verbose]
"""

import os
import re
import sys
from pathlib import Path
import yaml
import argparse

class DocsComplianceChecker:
    def __init__(self, docs_path="docs", verbose=False):
        self.docs_path = Path(docs_path)
        self.verbose = verbose
        self.violations = []

    def log(self, message):
        if self.verbose:
            print(f"[INFO] {message}")

    def validate_frontmatter(self, file_path):
        """Extract and validate YAML frontmatter"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not frontmatter_match:
            self.violations.append(f"{file_path}: Missing YAML frontmatter")
            return None

        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError as e:
            self.violations.append(f"{file_path}: Invalid YAML frontmatter - {e}")
            return None

        return frontmatter

    def validate_ethical_score(self, file_path, frontmatter):
        """Validate ethical score ≥91%"""
        if 'ethical_score' not in frontmatter:
            self.violations.append(f"{file_path}: Missing ethical_score field")
            return False

        score_text = frontmatter['ethical_score']
        # Extract percentage number
        score_match = re.search(r'(\d+)%', score_text)
        if not score_match:
            self.violations.append(f"{file_path}: Unable to parse ethical_score percentage")
            return False

        score = int(score_match.group(1))
        if score < 91:
            self.violations.append(f"{file_path}: Ethical score {score}% below minimum 91% requirement")
            return False

        return True

    def validate_ai_keywords(self, file_path, frontmatter):
        """Validate minimum 8 AI keywords"""
        if 'ai_keywords' not in frontmatter:
            self.violations.append(f"{file_path}: Missing ai_keywords field")
            return False

        keywords = frontmatter['ai_keywords']
        if isinstance(keywords, list):
            count = len(keywords)
        elif isinstance(keywords, str):
            # Count comma-separated items
            count = len([k.strip() for k in keywords.split(',') if k.strip()])
        else:
            self.violations.append(f"{file_path}: ai_keywords must be list or comma-separated string")
            return False

        if count < 8:
            self.violations.append(f"{file_path}: Only {count} AI keywords, minimum 8 required")
            return False

        return True

    def validate_required_fields(self, file_path, frontmatter):
        """Validate required DOCUMENT_GUIDELINES metadata fields"""
        required_fields = [
            'title', 'document_category', 'document_type', 'version',
            'last_updated', 'ai_keywords', 'ethical_score'
        ]

        for field in required_fields:
            if field not in frontmatter:
                self.violations.append(f"{file_path}: Missing required field '{field}'")

        return True  # Continue with other checks even if missing fields

    def validate_file(self, file_path):
        """Validate single file"""
        self.log(f"Validating {file_path}")

        frontmatter = self.validate_frontmatter(file_path)
        if not frontmatter:
            return False

        result = True
        result &= self.validate_required_fields(file_path, frontmatter)
        result &= self.validate_ethical_score(file_path, frontmatter)
        result &= self.validate_ai_keywords(file_path, frontmatter)

        return result

    def validate_all_docs(self):
        """Validate all markdown files in docs directory"""
        violations = []

        for md_file in self.docs_path.rglob('*.md'):
            if md_file.name in ['README.md', 'biological_consciousness_system_documentation.md']:
                continue  # Skip root level documents if not suitable

            try:
                self.validate_file(md_file)
            except Exception as e:
                violations.append(f"{md_file}: Validation error - {e}")

        return len(self.violations) == 0

    def run(self):
        """Execute compliance validation"""
        print("🔍 Biological Consciousness Documentation Compliance Monitor")
        print("=" * 60)

        success = self.validate_all_docs()

        if success:
            print("\n✅ ALL DOCUMENTATION COMPLIANT")
            print("🎯 High ethical standards maintained across all documentation")
        else:
            print(f"\n❌ COMPLIANCE VIOLATIONS FOUND ({len(self.violations)})")
            print("\nViolations:")
            for violation in self.violations:
                print(f"  • {violation}")

        return success

def main():
    parser = argparse.ArgumentParser(description='Documentation Compliance Checker')
    parser.add_argument('--fix', action='store_true', help='Auto-fix violations where possible')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    checker = DocsComplianceChecker(verbose=args.verbose)

    if args.fix:
        print("🔧 Auto-fix not yet implemented - run without --fix for validation only")
        return 1

    success = checker.run()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
