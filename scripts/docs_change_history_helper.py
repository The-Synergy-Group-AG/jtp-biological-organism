#!/usr/bin/env python3
"""
Documentation Change History Generator

Assists with creating standardized change history entries for ethical accountability.
Generates properly formatted change history lines with ethical impact assessment.

Usage:
    python docs_change_history_helper.py [options]

Options:
    --generate-change-entry  Generate a change history table row
    --ethical-impact-assessment  Assess ethical impact of proposed changes
    --validate-change-history  Validate existing change history format
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
import yaml

class ChangeHistoryHelper:
    def __init__(self):
        self.change_categories = {
            'CONTENT_UPDATES': '📈 Content revisions requiring ethical re-evaluation',
            'METADATA_CHANGES': '🔧 Metadata/structure modifications',
            'COMPLIANCE_CORRECTIONS': '⚖️ Ethical score improvements or corrections',
            'TEMPLATE_STANDARDIZATION': '📝 Format/consistency updates',
            'VIOLATION_FIXES': '🚫 Corrections for compliance violations',
            'APPROVAL_UPDATES': '✅ Status changes and approvals',
            'AUDIT_IMPROVEMENTS': '🔍 Audit trail enhancements',
            'DOC_TEMPLATE_CREATION': '📋 New document template creation'
        }

        self.ethical_impacts = {
            'NEW_DOCUMENT': 'N/A (New Document:',
            'IMPACT_HIGH': 'Changes affecting ethical scoring components (>5 point change)',
            'IMPACT_MEDIUM': 'Significant content changes with 3-5 point score effect',
            'IMPACT_LOW': 'Minor formatting/clarity improvements (1-2 point effect)',
            'IMPACT_NONE': 'No ethical scoring impact (technical/formatting only)'
        }

    def generate_change_entry(self,
                            version="1.0.0",
                            author="Documentation Team",
                            change_category="CONTENT_UPDATES",
                            ethical_impact="IMPACT_MEDIUM",
                            reviewer="GODHOOD Technical Review Board",
                            approval_notes="Compliance verified",
                            description="Document updates applied",
                            new_score=None):
        """Generate a formatted change history table row"""

        # Format version and date
        date = datetime.now().strftime("%Y-%m-%d")

        # Format ethical impact
        if ethical_impact == "NEW_DOCUMENT" and new_score:
            ethical_display = f"{ethical_impact}: {new_score} ✓)"
        else:
            ethical_display = f"{ethical_impact}: {self.ethical_impacts[ethical_impact]}"

        # Format change category
        category_display = f"{change_category}: {self.change_categories[change_category]}"

        # Generate the table row
        entry = f"| **{version}** | **{date}** | **{author}** | **{category_display}** | **{ethical_display}** | **{reviewer}** | **{approval_notes}** | **{description}** |"

        print("\n🔄 Generated Change History Entry:")
        print("="*100)
        print(entry)
        print("="*100)

        print("\n📋 Complete Change History Table Format:")
        print("""
#### **Enhanced Audit Trail - Change History with Ethical Accountability**

| **Version** | **Date** | **Author** | **Change Category** | **Ethical Impact** | **Reviewer** | **Approval Notes** | **Description of Changes** |
|-------------|----------|------------|-------------------|-------------------|--------------|-------------------|---------------------------|
""" + entry + """

### **Enhanced Change History Requirements**

#### **Mandated Change History Fields:**
1. **Version**: Semantic versioning (MAJOR.MINOR.PATCH)
2. **Date**: ISO format (YYYY-MM-DD)
3. **Author**: Name and role (e.g., "John Smith, AI Ethics Reviewer")
4. **Change Category**: Categorization of change type
5. **Ethical Impact**: New ethical score and impact assessment
6. **Reviewer**: Peer reviewer identity and qualification
7. **Approval Notes**: Signed approval with compliance confirmation
8. **Description**: Technical description of changes made
""")

        return entry

    def assess_ethical_impact(self, changes_description, current_score=90):
        """Assess the ethical impact of proposed changes"""

        print(f"🎯 Ethical Impact Assessment for Proposed Changes")
        print(f"Current Document Score: {current_score}%")
        print(f"Changes Description: {changes_description}")
        print("-" * 80)

        # Analyze change description for ethical components
        ethical_components = {
            'verification': ['verify', 'confirm', 'validate', 'check', 'evidence'],
            'accuracy': ['accurate', 'correct', 'truth', 'fact', 'scope'],
            'transparency': ['transparent', 'disclose', 'limit', 'uncertainty', 'constraint'],
            'error_handling': ['correct', 'fix', 'address', 'resolve', 'error'],
            'prevention': ['prevent', 'guard', 'safeguard', 'systematic', 'process']
        }

        affected_components = []
        for component, keywords in ethical_components.items():
            if any(keyword in changes_description.lower() for keyword in keywords):
                affected_components.append(component)

        impact_level = self.determine_impact_level(len(affected_components), changes_description)

        print(f"Affected Ethical Components: {', '.join(affected_components) if affected_components else 'None detected'}")
        print(f"Predicted Ethical Impact: {impact_level.upper()}")

        score_change_prediction = {
            'IMPACT_HIGH': f"-3 to +3 points (current: {current_score}% → ~{current_score}%)",
            'IMPACT_MEDIUM': f"-2 to +2 points (current: {current_score}% → ~{current_score}%)",
            'IMPACT_LOW': f"-1 to +1 points (current: {current_score}% → ~{current_score}%)",
            'IMPACT_NONE': f"No significant change (current: {current_score}% → ~{current_score}%)"
        }

        print(f"Predicted Score Change: {score_change_prediction[impact_level]}")

        print("\n⚖️ Recommended Change History Category:")
        recommendations = {
            'IMPACT_HIGH': ['COMPLIANCE_CORRECTIONS', 'CONTENT_UPDATES'],
            'IMPACT_MEDIUM': ['CONTENT_UPDATES', 'TEMPLATE_STANDARDIZATION'],
            'IMPACT_LOW': ['TEMPLATE_STANDARDIZATION', 'METADATA_CHANGES'],
            'IMPACT_NONE': ['METADATA_CHANGES', 'TEMPLATE_STANDARDIZATION']
        }

        print(f"• {', OR '.join(recommendations[impact_level])}")

        return impact_level

    def determine_impact_level(self, affected_count, description):
        """Determine ethical impact level based on analysis"""

        # High impact patterns
        high_patterns = ['ethical', 'compliance', 'score', 'review', 'audit', 'correction', 'violation']
        medium_patterns = ['content', 'update', 'revision', 'improvement', 'enhancement', 'standardization']
        low_patterns = ['format', 'style', 'grammar', 'typo', 'spelling', 'clarity']

        desc_lower = description.lower()

        if any(pattern in desc_lower for pattern in high_patterns) or affected_count >= 3:
            return 'IMPACT_HIGH'
        elif any(pattern in desc_lower for pattern in medium_patterns) or affected_count >= 2:
            return 'IMPACT_MEDIUM'
        elif any(pattern in desc_lower for pattern in low_patterns) or affected_count >= 1:
            return 'IMPACT_LOW'
        else:
            return 'IMPACT_NONE'

    def validate_change_history(self, file_path):
        """Validate change history format in a document"""

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return False

        # Find change history section
        history_match = re.search(r'#### \*\*Enhanced Audit Trail.*?\n\n(.*?)\n\n###', content, re.DOTALL)
        if not history_match:
            # Try old format
            history_match = re.search(r'#### \*\*Change History\*\*\n\n\|.*?\n\|.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
            if not history_match:
                print(f"❌ No change history section found in {file_path}")
                return False

        history_table = history_match.group(1)

        print(f"🔍 Validating change history for: {file_path}")

        # Check if new enhanced format
        if 'Ethical Impact' in history_table:
            print("✅ Enhanced audit trail format detected")

            # Check required columns
            required_headers = ['Ethical Impact', 'Change Category', 'Reviewer', 'Approval Notes']
            missing = [header for header in required_headers if header not in history_table]

            if missing:
                print(f"❌ Missing required columns: {missing}")
                return False
            else:
                print("✅ All required audit trail columns present")
        else:
            print("⚠️ Old format detected - consider upgrading to enhanced audit trail")

        # Check for version entries
        version_count = len(re.findall(r'\*\*\d+\.\d+\.\d+\*\*', history_table))
        print(f"📊 Change history entries: {version_count}")

        return True

def main():
    parser = argparse.ArgumentParser(description='Documentation Change History Helper')
    parser.add_argument('--generate-change-entry', action='store_true',
                       help='Generate a new change history table row')
    parser.add_argument('--ethical-impact-assessment', metavar='CHANGES_DESC',
                       help='Assess ethical impact of proposed changes')
    parser.add_argument('--validate-change-history', metavar='FILE_PATH',
                       help='Validate change history format in document')
    parser.add_argument('--version', default='1.0.0', help='Version number for entry')
    parser.add_argument('--author', default='Documentation Team', help='Author name')
    parser.add_argument('--category', choices=['CONTENT_UPDATES', 'METADATA_CHANGES',
                                              'COMPLIANCE_CORRECTIONS', 'TEMPLATE_STANDARDIZATION',
                                              'VIOLATION_FIXES', 'APPROVAL_UPDATES',
                                              'AUDIT_IMPROVEMENTS', 'DOC_TEMPLATE_CREATION'],
                       default='CONTENT_UPDATES', help='Change category')

    args = parser.parse_args()

    helper = ChangeHistoryHelper()

    if args.generate_change_entry:
        helper.generate_change_entry(
            version=args.version,
            author=args.author,
            change_category=args.category
        )
    elif args.ethical_impact_assessment:
        helper.assess_ethical_impact(args.ethical_impact_assessment)
    elif args.validate_change_history:
        helper.validate_change_history(args.validate_change_history)
    else:
        print("\n🔄 Documentation Change History Helper")
        print("Use --help for command options")
        print("\nQuick Examples:")
        print("  python docs_change_history_helper.py --ethical-impact-assessment 'Added ethical transparency section'")
        print("  python docs_change_history_helper.py --generate-change-entry --category COMPLIANCE_CORRECTIONS")
        print("  python docs_change_history_helper.py --validate-change-history DOCUMENT_GUIDELINES.md")

if __name__ == '__main__':
    main()
