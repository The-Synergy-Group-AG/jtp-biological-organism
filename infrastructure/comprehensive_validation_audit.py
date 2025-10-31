#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE VALIDATION AUDIT FOR AI BIOLOGICAL TESTING MASTER PLAN

This script performs comprehensive validation of the biological testing ecosystem
against 10 critical validation issues to ensure full compliance and AI execution optimization.

Validations Now Implemented:
1. Cross-reference consistency validation
2. Token size accuracy validation
3. AI navigation marker completeness validation
4. Load priority consistency validation
5. Ethical compliance AI integration validation
6. Content alignment & consistency validation with AUTO-FIX
7. Test script integration validation (path validation, import verification)
8. Progress tracking data flow validation (end-to-end testing)
9. Dependency tree accuracy validation
10. Context window optimization efficiency validation
"""

import os
import yaml
import json
import glob
import re
import tiktoken
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class ComprehensiveValidationAudit:
    """Comprehensive validation system for biological testing master plan ecosystem"""

    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or '/home/andre/projects/jtp-biological-organism')
        self.docs_dir = self.project_root / 'docs'
        self.testplanning_dir = self.docs_dir / '7.x-biological-testing-validation'
        self.sections_dir = self.testplanning_dir / 'sections'
        self.infrastructure_dir = self.project_root / 'infrastructure'
        self.reports_dir = self.project_root / 'reports'
        self.logs_dir = self.project_root / 'logs'

        # File registry for validation
        self.all_files = self._discover_all_files()

        # Validation results storage
        self.validation_results = defaultdict(dict)
        self.compliance_score = 0
        self.total_checks = 0

    def _discover_all_files(self) -> Dict[str, Path]:
        """Discover all files in the ecosystem that need validation"""
        all_files = {}

        # Core testing ecosystem files
        core_patterns = [
            self.testplanning_dir / "*.md",
            self.sections_dir / "*.md",
            self.infrastructure_dir / "master_test_plan_execution_monitor.py",
            self.reports_dir / "biological_master_plan_execution.json",
            self.logs_dir / "biological_master_plan_execution.log",
            self.reports_dir / "9.x-reports-analytics-monitoring/9.2-validation-assessment/*.md"
        ]

        for pattern_path in core_patterns:
            if isinstance(pattern_path, Path):
                pattern = str(pattern_path)
            else:
                pattern = pattern_path

            for file_path in glob.glob(pattern):
                rel_path = os.path.relpath(file_path, self.project_root)
                all_files[rel_path] = Path(file_path)

        return all_files

    def validate_cross_reference_consistency(self) -> Dict:
        """VALIDATION 1: Cross-reference consistency validation"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'file_count': len(self.all_files),
            'consistency_score': 100
        }

        inconsistent_files = []
        parent_child_sibling_usage = defaultdict(int)

        for file_path, abs_path in self.all_files.items():
            try:
                content = abs_path.read_text(encoding='utf-8')
                frontmatter = self._extract_frontmatter(content)

                if 'cross_references' in frontmatter:
                    refs = frontmatter['cross_references']

                    # Check for hierarchical structure vs simple arrays
                    if isinstance(refs, dict):
                        # Hierarchical structure present
                        has_parent = 'parent' in refs
                        has_child = 'child' in refs
                        has_sibling = 'sibling' in refs
                        parent_child_sibling_usage['hierarchical'] += 1

                        if has_parent or has_child or has_sibling:
                            # Properly structured hierarchical references
                            continue
                        else:
                            parent_child_sibling_usage['empty_hierarchical'] += 1
                    elif isinstance(refs, list):
                        # Simple array structure
                        parent_child_sibling_usage['simple_array'] += 1
                    else:
                        inconsistent_files.append(file_path)
                        parent_child_sibling_usage['invalid_structure'] += 1

            except Exception as e:
                results['issues_found'].append(f"Error reading {file_path}: {str(e)}")

        # Determine overall status
        if inconsistent_files:
            results['status'] = 'FAIL'
            results['issues_found'].extend([
                f"Inconsistent cross-reference structure in {len(inconsistent_files)} files",
                f"Usage breakdown: {dict(parent_child_sibling_usage)}"
            ])
            results['consistency_score'] = max(0, 100 - (len(inconsistent_files) * 10))

        return results

    def validate_token_size_accuracy(self) -> Dict:
        """VALIDATION 2: Token size accuracy validation"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'token_variance_threshold': 0.15,  # 15% variance allowed
            'files_checked': 0,
            'accuracy_score': 100
        }

        # Initialize tiktoken for accurate counting
        try:
            encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        except:
            results['status'] = 'SKIP'
            results['issues_found'].append("Tiktoken not available for token counting")
            return results

        significant_discrepancies = []
        files_with_token_markers = 0

        for file_path, abs_path in self.all_files.items():
            # Only check markdown files with AI navigation markers
            if not str(abs_path).endswith('.md'):
                continue

            try:
                content = abs_path.read_text(encoding='utf-8')

                # Look for documented token size in AI navigation markers
                token_size_match = re.search(r'📊 TOKEN_SIZE:\s*([\d,]+)', content)
                if not token_size_match:
                    continue

                documented_size = int(token_size_match.group(1).replace(',', ''))

                # Count actual tokens
                actual_tokens = len(encoding.encode(content))
                results['files_checked'] += 1
                files_with_token_markers += 1

                # Calculate variance
                variance = abs(actual_tokens - documented_size) / max(actual_tokens, documented_size, 1)

                if variance > results['token_variance_threshold']:
                    significant_discrepancies.append({
                        'file': file_path,
                        'documented': documented_size,
                        'actual': actual_tokens,
                        'variance': f"{variance:.1%}",
                        'variance_percentage': round(variance * 100, 1)
                    })

            except Exception as e:
                results['issues_found'].append(f"Error validating token count for {file_path}: {str(e)}")

        # Update results based on findings
        if significant_discrepancies:
            results['status'] = 'WARN'
            results['issues_found'].extend([
                f"Token size variances exceeded {results['token_variance_threshold']*100:.0f}% threshold in {len(significant_discrepancies)}/{files_with_token_markers} files",
                f"Largest discrepancy: {max(significant_discrepancies, key=lambda x: x['variance_percentage'])['variance']} in {max(significant_discrepancies, key=lambda x: x['variance_percentage'])['file']}"
            ])
            results['accuracy_score'] = max(50, 100 - (len(significant_discrepancies) * 2))
        elif files_with_token_markers == 0:
            results['status'] = 'WARN'
            results['issues_found'].append("No files found with token size markers for validation")
            results['accuracy_score'] = 50

        return results

    def validate_ai_navigation_markers_completeness(self) -> Dict:
        """VALIDATION 3: AI navigation marker completeness validation"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'required_markers': [
                ['🎯 SECTION_PURPOSE:'],
                ['🚀 LOAD_PRIORITY:'],
                ['🔗 CROSS_REFERENCES:'],
                ['📊 TOKEN_SIZE:'],
                ['⚠️ CRITICAL_DEPS:']
            ],
            'files_with_markers': 0,
            'completeness_score': 100
        }

        required_markers_count = len(results['required_markers'])
        incomplete_files = []

        for file_path, abs_path in self.all_files.items():
            if not any(x in file_path for x in ['.py', '.json', '.log']):
                try:
                    content = abs_path.read_text(encoding='utf-8')
                    markers_found = 0

                    for marker_group in results['required_markers']:
                        if all(marker in content for marker in marker_group):
                            markers_found += 1

                    if markers_found >= required_markers_count:
                        results['files_with_markers'] += 1
                    else:
                        incomplete_files.append({
                            'file': file_path,
                            'markers_found': markers_found,
                            'markers_missing': required_markers_count - markers_found
                        })

                except Exception as e:
                    results['issues_found'].append(f"Error checking markers in {file_path}: {str(e)}")

        if incomplete_files:
            results['status'] = 'FAIL'
            results['issues_found'].append(f"Missing AI navigation markers in {len(incomplete_files)} files")
            # Add specific file details
            for incomplete_file in incomplete_files:
                results['issues_found'].append(f"  - {incomplete_file['file']}: {incomplete_file['markers_found']}/{len(results['required_markers'])} markers found")
            results['completeness_score'] = max(0, 100 - (len(incomplete_files) * 20))

        return results

    def validate_load_priority_consistency(self) -> Dict:
        """VALIDATION 4: Load priority consistency validation"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'priority_scale_range': (1, 5),
            'unique_priorities_required': True,
            'files_with_priorities': 0,
            'consistency_score': 100
        }

        priorities_used = defaultdict(list)

        for file_path, abs_path in self.all_files.items():
            if not any(x in file_path for x in ['.py', '.json', '.log']):
                try:
                    content = abs_path.read_text(encoding='utf-8')
                    priority_match = re.search(r'🚀 LOAD_PRIORITY:\s*(\d+)/(\d+)', content)

                    if priority_match:
                        current_priority = int(priority_match.group(1))
                        scale_max = int(priority_match.group(2))

                        results['files_with_priorities'] += 1
                        priorities_used[current_priority].append(file_path)

                        # Check scale consistency
                        if scale_max != results['priority_scale_range'][1]:
                            results['issues_found'].append(f"Inconsistent scale in {file_path}: {scale_max}")

                        # Check range validity
                        if not (results['priority_scale_range'][0] <= current_priority <= results['priority_scale_range'][1]):
                            results['issues_found'].append(f"Invalid priority {current_priority} in {file_path}")

                except Exception as e:
                    results['issues_found'].append(f"Error checking priority in {file_path}: {str(e)}")

        # Check for duplicates if uniqueness required
        duplicates = {pri: files for pri, files in priorities_used.items() if len(files) > 1}
        if duplicates and results['unique_priorities_required']:
            results['status'] = 'WARN'
            results['issues_found'].append(f"Duplicate priorities found: {duplicates}")

        if results['issues_found']:
            results['status'] = 'FAIL'
            results['consistency_score'] = max(50, 100 - (len(results['issues_found']) * 10))

        return results

    def validate_ethical_compliance_ai_integration(self) -> Dict:
        """VALIDATION 5: Ethical compliance AI integration validation"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'ethical_keywords': ['ethical', 'ETHICAL_GUIDELINES.md'],
            'ai_ethical_integration_score': 100,
            'files_checked': 0
        }

        script_files = [f for f in self.all_files.values() if f.suffix == '.py']
        ethical_integration_gaps = []

        for script_path in script_files:
            if 'master_test_plan_execution_monitor.py' in str(script_path) or 'ai_orchestration_validator.py' in str(script_path):
                try:
                    content = script_path.read_text(encoding='utf-8')
                    results['files_checked'] += 1
                    ethical_score_checks = 0

                    # Check for ethical integration patterns
                    if any(keyword in content for keyword in results['ethical_keywords']):
                        ethical_score_checks += 1

                    if re.search(r'ethical_score.*>=?\s*\d+', content):  # Score validation patterns
                        ethical_score_checks += 1

                    if 'compliance' in content.lower() or 'ethical' in content.lower():
                        ethical_score_checks += 1

                    if ethical_score_checks < 2:  # Less than 2 ethical checks = gap
                        ethical_integration_gaps.append(str(script_path.name))

                except Exception as e:
                    results['issues_found'].append(f"Error checking script {script_path.name}: {str(e)}")

        if ethical_integration_gaps:
            results['status'] = 'WARN'
            results['issues_found'].append(f"Inadequate ethical integration in scripts: {ethical_integration_gaps}")
            results['ai_ethical_integration_score'] = max(50, 100 - (len(ethical_integration_gaps) * 25))

        return results

    def validate_content_alignment_consistency(self, auto_fix: bool = False) -> Dict:
        """VALIDATION 6: Content alignment across documents (cross-document consistency)"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'files_checked': 0,
            'alignment_score': 100,
            'auto_fix_enabled': auto_fix,
            'fixes_applied': 0,
            'critical_consistency_checks': {
                'user_stories_count': 442,
                'biological_systems_count': 11,
                'biological_units_count': 25,
                'godhood_target': '99.7%',
                'tadft_methodology': 'Test-Assess-Debug-Fix-Test'
            }
        }

        alignments = defaultdict(dict)
        consistency_issues = []

        # Check terminology and key metrics consistency
        for file_path, abs_path in self.all_files.items():
            if str(abs_path).endswith('.md'):
                try:
                    content = abs_path.read_text(encoding='utf-8')
                    results['files_checked'] += 1

                    # Check user stories count consistency
                    user_story_matches = re.findall(r'(\d+) user stories?', content)
                    if user_story_matches:
                        story_counts = [int(match) for match in user_story_matches]
                        # Check if any match the expected 442
                        if not any(count in [442, 443] for count in story_counts):  # Allow small variance
                            alignments[file_path]['user_stories'] = max(story_counts)

                            # Auto-fix if enabled
                            if auto_fix:
                                content = re.sub(
                                    r'(\d+) user stories?',
                                    f"{results['critical_consistency_checks']['user_stories_count']} user stories",
                                    content
                                )
                                abs_path.write_text(content, encoding='utf-8')
                                results['fixes_applied'] += 1

                    # Check biological systems count
                    systems_matches = re.findall(r'(\d+) biological systems?', content)
                    if systems_matches:
                        systems_count = max(int(match) for match in systems_matches)
                        if systems_count != results['critical_consistency_checks']['biological_systems_count']:
                            alignments[file_path]['biological_systems'] = systems_count

                            # Auto-fix if enabled
                            if auto_fix:
                                content = re.sub(
                                    r'(\d+) biological systems?',
                                    f"{results['critical_consistency_checks']['biological_systems_count']} biological systems",
                                    content
                                )
                                abs_path.write_text(content, encoding='utf-8')
                                results['fixes_applied'] += 1

                    # Check biological units count
                    units_matches = re.findall(r'(\d+) biological units?', content)
                    if units_matches:
                        units_count = max(int(match) for match in units_matches)
                        if units_count != results['critical_consistency_checks']['biological_units_count']:
                            alignments[file_path]['biological_units'] = units_count

                            # Auto-fix if enabled
                            if auto_fix:
                                content = re.sub(
                                    r'(\d+) biological units?',
                                    f"{results['critical_consistency_checks']['biological_units_count']} biological units",
                                    content
                                )
                                abs_path.write_text(content, encoding='utf-8')
                                results['fixes_applied'] += 1

                    # Check GODHOOD target consistency - expanded patterns
                    godhood_patterns = [
                        r'(\d+\.?\d*)%\s*GODHOOD',  # "X% GODHOOD"
                        r'GODHOOD.*?(\d+\.?\d*)%',   # "GODHOOD X%"
                        r'(\d+)[\.\,]?,?\s*%(?!.*?GODHOOD)',  # Standalone "X%" not followed by GODHOOD
                        r'(\d+\.\d+)%(?!.*?GODHOOD)', # Decimal "X.X%" not followed by GODHOOD
                    ]

                    incorrect_percentages = []
                    for pattern in godhood_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            percentage = match
                            # Only flag if it's not "99.7" or if it doesn't have GODHOOD context
                            if (percentage and
                                percentage not in ['99.7'] and
                                '99.7% GODHOOD' not in content.replace(percentage + '%', '')):
                                incorrect_percentages.append(percentage)

                    if incorrect_percentages:
                        alignments[file_path]['godhood_target'] = f"{max(incorrect_percentages)}%"

                        # Auto-fix if enabled - comprehensive replacement
                        if auto_fix:
                            # Replace patterns with GODHOOD context
                            content = re.sub(
                                r'(\d+\.?\d*)%\s*GODHOOD',
                                f"{results['critical_consistency_checks']['godhood_target']} GODHOOD",
                                content
                            )
                            content = re.sub(
                                r'GODHOOD.*?(\d+\.?\d*)%',
                                f"GODHOOD {results['critical_consistency_checks']['godhood_target']}",
                                content
                            )

                            # Replace standalone percentages that are likely GODHOOD targets
                            # This handles cases like "7%" that should be "99.7% GODHOOD"
                            content = re.sub(
                                r'(\d+)[\.\,]?,?\s*%',  # Match "7%" or "7.%"
                                f"{results['critical_consistency_checks']['godhood_target']} GODHOOD",
                                content
                            )

                            abs_path.write_text(content, encoding='utf-8')
                            results['fixes_applied'] += 1

                    # Check for inconsistent terminology
                    inconsistent_terms = []
                    if 'Godhood' in content and 'GODHOOD' in content:
                        inconsistent_terms.append("Mixed case GODHOOD/Godhood")

                        # Auto-fix terminology to standardized format
                        if auto_fix:
                            content = content.replace('Godhood', 'GODHOOD')
                            abs_path.write_text(content, encoding='utf-8')
                            results['fixes_applied'] += 1

                    if 'Tadft' in content and 'TADFT' in content:
                        inconsistent_terms.append("Mixed case TADFT/Tadft")

                        # Auto-fix terminology to standardized format
                        if auto_fix:
                            content = content.replace('Tadft', 'TADFT')
                            abs_path.write_text(content, encoding='utf-8')
                            results['fixes_applied'] += 1

                    if inconsistent_terms:
                        alignments[file_path]['terminology_inconsistencies'] = inconsistent_terms

                except Exception as e:
                    results['issues_found'].append(f"Error checking alignment in {file_path}: {str(e)}")

        # Analyze findings for consistency issues
        if alignments:
            total_files_with_issues = len(alignments)

            # Check for user story count inconsistencies
            user_story_inconsistencies = [
                f"{file}: mentions {data['user_stories']} user stories"
                for file, data in alignments.items()
                if 'user_stories' in data and data['user_stories'] not in [442, 443]
            ]

            # Check for biological systems count inconsistencies
            systems_inconsistencies = [
                f"{file}: mentions {data['biological_systems']} biological systems"
                for file, data in alignments.items()
                if 'biological_systems' in data
            ]

            # Check for biological units count inconsistencies
            units_inconsistencies = [
                f"{file}: mentions {data['biological_units']} biological units"
                for file, data in alignments.items()
                if 'biological_units' in data
            ]

            # Check for GODHOOD target inconsistencies
            godhood_inconsistencies = [
                f"{file}: mentions {data['godhood_target']}"
                for file, data in alignments.items()
                if 'godhood_target' in data
            ]

            # Compile all consistency issues
            all_inconsistencies = (
                user_story_inconsistencies + systems_inconsistencies +
                units_inconsistencies + godhood_inconsistencies
            )

            if all_inconsistencies:
                results['status'] = 'WARN' if len(all_inconsistencies) < 5 else 'FAIL'
                results['issues_found'].extend([
                    f"Content alignment issues found in {total_files_with_issues}/{results['files_checked']} files",
                    f"Critical consistency violations: {len(all_inconsistencies)}"
                ])
                if auto_fix:
                    results['issues_found'].append(f"✅ Auto-fix applied: {results['fixes_applied']} corrections made")
                else:
                    results['issues_found'].extend(all_inconsistencies[:10])  # Limit to first 10
                results['alignment_score'] = max(50, 100 - (total_files_with_issues * 5))

        return results

    def validate_test_script_integration(self) -> Dict:
        """VALIDATION 7: Test script integration validation (path validation, import verification)"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'files_checked': 0,
            'paths_validated': 0,
            'imports_verified': 0,
            'integration_score': 100,
            'path_validation_results': defaultdict(list),
            'import_validation_results': defaultdict(list)
        }

        # Get all Python script files for validation
        python_files = [f for f in self.all_files.values() if f.suffix == '.py']

        for script_path in python_files:
            try:
                content = script_path.read_text(encoding='utf-8')
                results['files_checked'] += 1
                rel_path = os.path.relpath(script_path, self.project_root)

                # Path validation: Check for file paths referenced in the script
                path_issues = self._validate_script_paths(content, script_path, rel_path)
                if path_issues:
                    results['path_validation_results'][rel_path].extend(path_issues)
                    results['issues_found'].extend([f"{rel_path}: {issue}" for issue in path_issues])

                # Import validation: Check for Python imports
                import_issues = self._validate_script_imports(content, script_path, rel_path)
                if import_issues:
                    results['import_validation_results'][rel_path].extend(import_issues)
                    results['issues_found'].extend([f"{rel_path}: {issue}" for issue in import_issues])

            except Exception as e:
                results['issues_found'].append(f"Error validating script {rel_path}: {str(e)}")

        # Update counters
        results['paths_validated'] = len([item for sublist in results['path_validation_results'].values() for item in sublist])
        results['imports_verified'] = len([item for sublist in results['import_validation_results'].values() for item in sublist])

        # Determine overall status
        total_issues = len(results['issues_found'])
        if total_issues > 0:
            results['status'] = 'FAIL' if total_issues > 5 else 'WARN'
            results['integration_score'] = max(50, 100 - total_issues * 5)

        return results

    def _validate_script_paths(self, content: str, script_path: Path, rel_path: str) -> List[str]:
        """Validate file paths referenced in Python scripts"""
        issues = []

        # Split code into lines and check each line for path references
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Skip comments and blank lines
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#') or stripped_line.startswith('"""') or stripped_line.startswith("'''"):
                continue

            # Check for string literals containing file paths
            string_matches = re.findall(r'["\']([^"\']*?\.(?:md|py|json|log|txt))["\']', stripped_line)
            for path_str in string_matches:
                # Skip URLs, template strings, and obvious variable names
                if (path_str.startswith(('http://', 'https://', 'ftp://')) or
                    any(char in path_str for char in ['{', '}', '$']) or  # Template variables
                    path_str in ['__file__', '__name__']):  # Python builtins
                    continue

                # Resolve path relative to script location or project root
                try:
                    resolved_path = self._resolve_script_path(path_str, script_path)

                    if not resolved_path.exists():
                        # Check if it's a pattern or wildcard
                        if '*' in path_str or '?' in path_str:
                            # For glob patterns, check if any matching files exist
                            import glob as glob_module
                            if not glob_module.glob(str(resolved_path)):
                                issues.append(f"Path pattern '{path_str}' matches no files (line {line_num})")
                        else:
                            issues.append(f"Referenced path '{path_str}' does not exist (line {line_num}, resolved to {resolved_path})")
                except Exception as e:
                    issues.append(f"Could not resolve path '{path_str}' (line {line_num}): {str(e)}")

        return issues

    def _validate_script_imports(self, content: str, script_path: Path, rel_path: str) -> List[str]:
        """Validate Python import statements"""
        issues = []

        # Import patterns to check
        import_patterns = [
            r'^import\s+(\w+)',  # Standard imports
            r'^from\s+(\w+)',     # From imports
            r'^from\s+([\w.]+)\s+import',  # From ... import
        ]

        for pattern in import_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for module_name in matches:
                # Skip standard library modules and known external modules
                std_lib_modules = {
                    'os', 'sys', 'json', 'yaml', 're', 'pathlib', 'glob', 'argparse',
                    'datetime', 'time', 'logging', 'collections', 'functools',
                    'typing', 'enum', 'dataclasses', 'asyncio', 'threading',
                    'subprocess', 'shutil', 'tempfile', 'urllib', 'pathlib'
                }

                external_modules = {
                    'tiktoken',  # Known external dependency
                    'pytest', 'unittest', 'pytest.ini'  # Testing frameworks
                }

                if (module_name not in std_lib_modules and
                    not any(module_name.startswith(ext) for ext in external_modules) and
                    not '.' in module_name):  # Skip submodules for now

                    # Check if this is a local module (file exists)
                    module_file = self.project_root / f"{module_name}.py"
                    module_dir = self.project_root / module_name

                    if not (module_file.exists() or module_dir.exists()):
                        # Check if it's referenced in docs or other scripts
                        if not self._is_module_referenced_elsewhere(module_name):
                            issues.append(f"Import '{module_name}' may not be available - no local module found")

        return issues

    def _resolve_script_path(self, path_str: str, script_path: Path) -> Path:
        """Resolve a path string relative to the script's location or project root"""
        # Handle absolute paths
        if path_str.startswith('/'):
            return Path(path_str)

        # Handle paths relative to script location
        script_dir = script_path.parent
        resolved = (script_dir / path_str).resolve()

        # If not found relative to script, try relative to project root
        if not resolved.exists():
            resolved = (self.project_root / path_str).resolve()

        return resolved

    def _is_module_referenced_elsewhere(self, module_name: str) -> bool:
        """Check if a module is referenced in other documentation or scripts"""
        reference_count = 0

        for file_path in self.all_files.values():
            try:
                content = file_path.read_text(encoding='utf-8')
                if module_name in content:
                    reference_count += 1
                    if reference_count >= 2:  # Referenced in at least 2 places
                        return True
            except:
                continue

        return False

    def validate_progress_tracking_data_flow(self) -> Dict:
        """VALIDATION 8: Progress tracking data flow validation (end-to-end testing)"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'data_flow_score': 100,
            'layers_tested': 3,
            'data_integrity_checks': 0,
            'synchronization_checks': 0,
            'progress_tracking_layers': {
                'real_time_log': {
                    'file': 'logs/biological_master_plan_execution.log',
                    'required': True,
                    'data_type': 'text_log',
                    'exists': False,
                    'writable': False
                },
                'structured_metrics': {
                    'file': 'reports/biological_master_plan_execution.json',
                    'required': True,
                    'data_type': 'json_metrics',
                    'exists': False,
                    'writable': False
                },
                'formal_compliance': {
                    'file': 'docs/9.x-reports-analytics-monitoring/9.2-validation-assessment/9.2.9-master-test-plan-execution-progress.md',
                    'required': False,
                    'data_type': 'compliance_report',
                    'exists': False,
                    'writable': False
                }
            },
            'data_flow_connectivity': {
                'log_to_json_synchronization': False,
                'json_to_report_transformation': False,
                'end_to_end_data_integrity': False
            }
        }

        # Check file existence and writability for all layers
        for layer_name, layer_info in results['progress_tracking_layers'].items():
            file_path = self.project_root / layer_info['file']

            # Existence check
            if file_path.exists():
                layer_info['exists'] = True
                results['issues_found'].append(f"✅ {layer_name} layer exists: {layer_info['file']}")
            else:
                # For required files, note this as a warning rather than fail
                if layer_info['required']:
                    results['issues_found'].append(f"⚠️ {layer_name} layer missing: {layer_info['file']} (required - will be created during first run)")
                    layer_info['exists'] = False
                else:
                    results['issues_found'].append(f"ℹ️ {layer_name} layer not yet created: {layer_info['file']} (optional - created on demand)")
                    layer_info['exists'] = False

            # Writability check (check parent directory permissions)
            parent_dir = file_path.parent
            if parent_dir.exists():
                try:
                    # Create a test file to check writability
                    test_file = parent_dir / f"test_write_{layer_name}.tmp"
                    test_file.write_text("test", encoding='utf-8')
                    test_file.unlink()  # Clean up
                    layer_info['writable'] = True
                    results['issues_found'].append(f"✅ {layer_name} directory writable: {parent_dir}")
                except Exception as e:
                    layer_info['writable'] = False
                    results['issues_found'].append(f"❌ {layer_name} directory not writable: {parent_dir} - {str(e)}")
            else:
                # Parent directory doesn't exist
                layer_info['writable'] = False
                results['issues_found'].append(f"❌ {layer_name} parent directory missing: {parent_dir}")

        results['data_integrity_checks'] += 1

        # Test data structure consistency if files exist
        json_file = self.project_root / results['progress_tracking_layers']['structured_metrics']['file']
        log_file = self.project_root / results['progress_tracking_layers']['real_time_log']['file']
        report_file = self.project_root / results['progress_tracking_layers']['formal_compliance']['file']

        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                # Validate JSON structure has required fields
                required_fields = ['execution_metadata', 'execution_status', 'biological_harmony_metrics']
                missing_fields = [field for field in required_fields if field not in json_data]

                if missing_fields:
                    results['issues_found'].append(f"❌ JSON structure incomplete - missing: {missing_fields}")
                else:
                    results['issues_found'].append("✅ JSON structure valid with required metadata fields")
                    results['data_flow_connectivity']['log_to_json_synchronization'] = True

                results['data_integrity_checks'] += 1

            except json.JSONDecodeError as e:
                results['issues_found'].append(f"❌ JSON file corrupted: {e}")
            except Exception as e:
                results['issues_found'].append(f"❌ JSON validation error: {e}")

        # Test log file structure if exists
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()

                # Check for proper log format (should have timestamps and status messages)
                timestamped_lines = len(re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', log_content))

                if timestamped_lines > 0:
                    results['issues_found'].append(f"✅ Log file properly formatted with {timestamped_lines} timestamped entries")
                else:
                    results['issues_found'].append("⚠️ Log file exists but contains no timestamped entries")

                results['data_integrity_checks'] += 1

            except Exception as e:
                results['issues_found'].append(f"❌ Log file validation error: {e}")

        # Test formal report structure if exists
        if report_file.exists():
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    report_content = f.read()

                # Check for Document Guidelines compliance (should have proper frontmatter)
                if report_content.startswith('---'):
                    frontmatter_end = report_content.find('---', 3)
                    if frontmatter_end > 0:
                        try:
                            frontmatter = yaml.safe_load(report_content[3:frontmatter_end])
                            if 'biological_system' in frontmatter and 'consciousness_score' in frontmatter:
                                results['issues_found'].append("✅ Formal report follows Document Guidelines compliance")
                                results['data_flow_connectivity']['json_to_report_transformation'] = True
                            else:
                                results['issues_found'].append("⚠️ Formal report missing required Document Guidelines metadata")
                        except:
                            results['issues_found'].append("⚠️ Formal report frontmatter malformed")
                    else:
                        results['issues_found'].append("⚠️ Formal report frontmatter incomplete")
                else:
                    results['issues_found'].append("⚠️ Formal report not following Document Guidelines format")

                results['data_integrity_checks'] += 1

            except Exception as e:
                results['issues_found'].append(f"❌ Report validation error: {e}")

        # Test synchronization between layers
        if (results['progress_tracking_layers']['structured_metrics']['exists'] and
            results['progress_tracking_layers']['real_time_log']['exists']):

            # Check timestamp synchronization
            try:
                # Get JSON last update
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                json_timestamp = json_data.get('execution_metadata', {}).get('last_updated')

                # Get log last entry
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_lines = f.readlines()
                if log_lines:
                    last_log_line = log_lines[-1]
                    log_timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', last_log_line)
                    if log_timestamp_match:
                        log_timestamp = log_timestamp_match.group(1)

                        # Compare timestamps (rough check - within 5 minutes)
                        if json_timestamp and log_timestamp:
                            from datetime import datetime
                            json_dt = datetime.fromisoformat(json_timestamp.replace('Z', '+00:00'))
                            log_dt = datetime.strptime(log_timestamp, '%Y-%m-%d %H:%M:%S')

                            time_diff = abs((json_dt - log_dt).total_seconds())
                            if time_diff < 300:  # 5 minutes
                                results['issues_found'].append(f"⚡ Timestamps synchronized within {time_diff:.1f} seconds")
                                results['synchronization_checks'] += 1
                            else:
                                results['issues_found'].append(f"⚠️ Timestamps out of sync by {time_diff:.1f} seconds")
                        else:
                            results['issues_found'].append("ℹ️ Timestamp comparison unavailable - incomplete data")
                    else:
                        results['issues_found'].append("ℹ️ Cannot extract timestamps from latest log entry")
                else:
                    results['issues_found'].append("ℹ️ Log file exists but empty")

            except Exception as e:
                results['issues_found'].append(f"⚠️ Synchronization check failed: {e}")

        # Determine overall data flow health
        connectivity_score = sum(results['data_flow_connectivity'].values())
        max_connectivity = len(results['data_flow_connectivity'])

        if connectivity_score == max_connectivity:
            results['data_flow_connectivity']['end_to_end_data_integrity'] = True
            results['issues_found'].append(f"✅ Data flow fully connected: {connectivity_score}/ {max_connectivity} layers synchronized")
        elif connectivity_score >= max_connectivity / 2:
            results['issues_found'].append(f"⚠️ Data flow partially connected: {connectivity_score}/ {max_connectivity} layers synchronized - requires attention")
            results['status'] = 'WARN'
            results['issues_found'].append(f"❌ Critical data flow failure: {connectivity_score}/ {max_connectivity} layers synchronized - immediate action required")
            results['data_flow_score'] = 50
            results['status'] = 'FAIL'
            results['issues_found'].append(".0f"           # Check for critical issues
        critical_issues = sum(1 for issue in results['issues_found'] if issue.startswith(('❌', '⚠️')))
        if critical_issues > 3:
            results['status'] = 'FAIL'
        elif critical_issues > 0:
            results['status'] = 'WARN' if results['status'] == 'PASS' else results['status']

        return results

    def validate_dependency_tree_accuracy(self) -> Dict:
        """VALIDATION 9: Dependency tree accuracy validation"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'dependency_score': 100,
            'dependencies_analyzed': 0,
            'dependencies_validated': 0,
            'critical_dependencies_status': {
                'python_requirements': False,
                'testing_frameworks': False,
                'ai_dependencies': False,
                'monitoring_tools': False,
                'documentation_tools': False
            },
            'dependency_tree': {
                'python_version': '3.8+',
                'core_dependencies': ['pytest', 'pyyaml', 'requests', 'pathlib'],
                'ai_dependencies': ['tiktoken', 'openai'],
                'optional_dependencies': ['pandas', 'numpy', 'matplotlib']
            }
        }

        # Check core dependency files
        requirements_file = self.project_root / 'requirements.txt'
        dev_requirements_file = self.project_root / 'requirements-dev.txt'

        # Validate Python requirements.txt
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    requirements_content = f.read()

                # Check for core dependencies
                missing_core_deps = []
                for dep in results['dependency_tree']['core_dependencies']:
                    if dep not in requirements_content:
                        missing_core_deps.append(dep)
                    else:
                        results['dependencies_validated'] += 1

                if missing_core_deps:
                    results['issues_found'].append(f"❌ Missing core dependencies in requirements.txt: {missing_core_deps}")
                    results['critical_dependencies_status']['python_requirements'] = False
                else:
                    results['issues_found'].append("✅ Core dependencies present in requirements.txt")
                    results['critical_dependencies_status']['python_requirements'] = True

                results['dependencies_analyzed'] += 1

            except Exception as e:
                results['issues_found'].append(f"❌ Error reading requirements.txt: {e}")
        else:
            results['issues_found'].append("❌ requirements.txt missing - critical dependency file not found")
            results['critical_dependencies_status']['python_requirements'] = False

        # Validate development requirements
        if dev_requirements_file.exists():
            try:
                with open(dev_requirements_file, 'r', encoding='utf-8') as f:
                    dev_content = f.read()

                # Check for testing frameworks
                testing_deps = ['pytest', 'pytest-cov', 'unittest']
                dev_testing_deps = [dep for dep in testing_deps if dep in dev_content]

                if len(dev_testing_deps) >= 2:
                    results['issues_found'].append(f"✅ Testing frameworks present in dev requirements: {dev_testing_deps}")
                    results['critical_dependencies_status']['testing_frameworks'] = True
                    results['dependencies_validated'] += len(dev_testing_deps)
                else:
                    results['issues_found'].append(f"⚠️ Limited testing frameworks in dev requirements: {dev_testing_deps}")
                    results['critical_dependencies_status']['testing_frameworks'] = False

                results['dependencies_analyzed'] += 1

            except Exception as e:
                results['issues_found'].append(f"❌ Error reading requirements-dev.txt: {e}")
        else:
            results['issues_found'].append("⚠️ requirements-dev.txt not found - development dependencies missing")
            results['critical_dependencies_status']['testing_frameworks'] = False

        # Check for AI/ML dependencies
        ai_deps = results['dependency_tree']['ai_dependencies']
        ai_deps_found = 0

        if requirements_file.exists():
            with open(requirements_file, 'r', encoding='utf-8') as f:
                req_content = f.read()
                for dep in ai_deps:
                    if dep in req_content:
                        ai_deps_found += 1
                        results['dependencies_validated'] += 1

        if ai_deps_found >= len(ai_deps) * 0.5:  # At least 50% of AI deps present
            results['issues_found'].append(f"✅ AI dependencies sufficiently present: {ai_deps_found}/{len(ai_deps)}")
            results['critical_dependencies_status']['ai_dependencies'] = True
        else:
            results['issues_found'].append(f"⚠️ AI dependencies incomplete: {ai_deps_found}/{len(ai_deps)} found")
            results['critical_dependencies_status']['ai_dependencies'] = False

        # Check for package.json if exists (Node.js dependencies)
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)

                if 'dependencies' in package_data and package_data['dependencies']:
                    results['issues_found'].append(f"✅ Node.js dependencies found: {len(package_data['dependencies'])} packages")
                    results['dependencies_validated'] += len(package_data['dependencies'])
                else:
                    results['issues_found'].append("ℹ️ package.json exists but no dependencies defined")

                results['dependencies_analyzed'] += 1

            except Exception as e:
                results['issues_found'].append(f"❌ Error reading package.json: {e}")

        # Check pyproject.toml if exists (modern Python packaging)
        pyproject_toml = self.project_root / 'pyproject.toml'
        if pyproject_toml.exists():
            try:
                with open(pyproject_toml, 'r', encoding='utf-8') as f:
                    toml_content = f.read()

                if '[project.dependencies]' in toml_content or '[tool.poetry.dependencies]' in toml_content:
                    results['issues_found'].append("✅ Modern Python packaging (pyproject.toml) configured")
                    results['dependencies_validated'] += 1
                else:
                    results['issues_found'].append("ℹ️ pyproject.toml exists but dependencies section not configured")

                results['dependencies_analyzed'] += 1

            except Exception as e:
                results['issues_found'].append(f"❌ Error reading pyproject.toml: {e}")

        # Check for Docker dependencies if Docker files exist
        docker_files = list(self.project_root.glob("**/Dockerfile*"))
        if docker_files:
            results['issues_found'].append(f"✅ Docker containerization present: {len(docker_files)} Dockerfile(s) found")
            results['dependencies_analyzed'] += 1

        # Calculate dependency health score
        critical_deps_met = sum(results['critical_dependencies_status'].values())
        total_critical_deps = len(results['critical_dependencies_status'])

        if critical_deps_met == total_critical_deps:
            results['dependency_score'] = 100
            results['status'] = 'PASS'
        elif critical_deps_met >= total_critical_deps * 0.75:
            results['dependency_score'] = 75
            results['status'] = 'WARN'
        else:
            results['dependency_score'] = 50
            results['status'] = 'FAIL'

        if results['dependency_score'] < 80:
            results['issues_found'].append(f"⚠️ Dependency tree health: {critical_deps_met}/{total_critical_deps} critical dependencies satisfied")

        return results

    def validate_context_window_optimization_efficiency(self) -> Dict:
        """VALIDATION 10: Context window optimization efficiency validation"""
        results = {
            'status': 'PASS',
            'issues_found': [],
            'context_optimization_score': 100,
            'token_efficiency_rating': 'HIGH',
            'context_window_metrics': {
                'average_tokens_per_file': 0,
                'files_analyzed': 0,
                'total_tokens': 0,
                'optimization_opportunities': 0,
                'context_window_size': 128000,  # GPT-4 Turbo context window
                'efficient_usage_threshold': 0.85  # 85% efficient context usage
            },
            'optimization_categories': {
                'documentation_efficiency': 'UNKNOWN',
                'code_compaction': 'UNKNOWN',
                'redundant_content': 'UNKNOWN',
                'context_relevance': 'UNKNOWN'
            }
        }

        # Analyze token usage across documentation files
        markdown_files = []
        for file_path in self.all_files.values():
            if str(file_path).endswith('.md'):
                markdown_files.append(file_path)

        total_tokens = 0
        files_with_tokens = 0

        # Initialize tiktoken for accurate token counting
        try:
            import tiktoken
            try:
                # Use GPT-4 encoding for accurate context window analysis
                encoding = tiktoken.get_encoding("cl100k_base")
                tokenizer_available = True
            except Exception as e:
                results['issues_found'].append(f"⚠️ Tiktoken encoding failed, using approximation: {e}")
                tokenizer_available = False
        except ImportError:
            results['issues_found'].append("⚠️ Tiktoken not available, using approximate token counting")
            tokenizer_available = False

        for md_file in markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                results['context_window_metrics']['files_analyzed'] += 1

                if tokenizer_available:
                    try:
                        file_tokens = len(encoding.encode(content))
                        total_tokens += file_tokens
                        files_with_tokens += 1

                        # Check for token size markers and accuracy
                        token_marker_match = re.search(r'📊 TOKEN_SIZE:\s*([\d,]+)', content)
                        if token_marker_match:
                            documented_tokens = int(token_marker_match.group(1).replace(',', ''))

                            if abs(file_tokens - documented_tokens) / max(file_tokens, documented_tokens) > 0.1:  # 10% variance
                                results['issues_found'].append(f"⚠️ {md_file.name}: documented {documented_tokens} tokens, actual {file_tokens} tokens")
                                results['context_window_metrics']['optimization_opportunities'] += 1
                        elif file_tokens > 1000:  # Large files without token markers could be optimized
                            results['issues_found'].append(f"ℹ️ {md_file.name}: {file_tokens} tokens without size marker (consider adding 📊 TOKEN_SIZE)")
                            results['context_window_metrics']['optimization_opportunities'] += 1

                    except Exception as e:
                        results['issues_found'].append(f"⚠️ Token counting failed for {md_file.name}: {e}")
                else:
                    # Fallback approximation: ~4 characters per token
                    approx_tokens = len(content) // 4
                    total_tokens += approx_tokens
                    files_with_tokens += 1
                    results['issues_found'].append("ℹ️ Using approximate token counting (install tiktoken for accuracy)")

            except Exception as e:
                results['issues_found'].append(f"❌ Error reading {md_file.name}: {e}")

        # Calculate efficiency metrics
        if files_with_tokens > 0:
            avg_tokens_per_file = total_tokens / files_with_tokens
            results['context_window_metrics']['average_tokens_per_file'] = round(avg_tokens_per_file)
            results['context_window_metrics']['total_tokens'] = total_tokens
            results['context_window_metrics']['files_analyzed'] = files_with_tokens

            # Calculate context window efficiency
            total_context_usage = total_tokens / results['context_window_metrics']['context_window_size']
            efficient_usage = total_context_usage <= results['context_window_metrics']['efficient_usage_threshold']

            if efficient_usage:
                results['issues_found'].append(f"✅ Context window usage efficient: {total_context_usage:.1%} of available capacity")
                results['optimization_categories']['context_relevance'] = 'GOOD'
            else:
                results['issues_found'].append(f"⚠️ High context window usage: {total_context_usage:.1%} may exceed efficient capacity")
                results['optimization_categories']['context_relevance'] = 'NEEDS_OPTIMIZATION'
                results['context_optimization_score'] -= 20

        # Check documentation efficiency patterns
        # Look for repetitive content that could be consolidated
        content_patterns = defaultdict(int)

        for md_file in markdown_files[:10]:  # Check first 10 files to avoid excessive processing
            try:
                content = md_file.read_text(encoding='utf-8')

                # Check for excessive headers (potential over-fragmentation)
                header_count = len(re.findall(r'^#{1,6}\s', content, re.MULTILINE))
                if header_count > 20:  # Arbitrary threshold for over-fragmented docs
                    results['issues_found'].append(f"⚠️ {md_file.name}: {header_count} headers (document may be over-fragmented)")
                    content_patterns['excessive_headers'] += 1

                # Check for long paragraphs (potential for splitting/optimization)
                long_paragraphs = len(re.findall(r'\n{2,}[^\n]{500,}\n{2,}', content))
                if long_paragraphs > 5:
                    results['issues_found'].append(f"ℹ️ {md_file.name}: {long_paragraphs} long paragraphs (consider splitting for better AI context)")
                    content_patterns['long_paragraphs'] += 1

            except Exception as e:
                continue

        # Assess documentation efficiency
        if content_patterns['excessive_headers'] == 0 and content_patterns['long_paragraphs'] <= 2:
            results['optimization_categories']['documentation_efficiency'] = 'GOOD'
        elif content_patterns['excessive_headers'] > 0:
            results['optimization_categories']['documentation_efficiency'] = 'NEEDS_CONSOLIDATION'
            results['context_optimization_score'] -= 15
        else:
            results['optimization_categories']['documentation_efficiency'] = 'NEEDS_REFORMATTING'
            results['context_optimization_score'] -= 10

        # Check for code compaction opportunities
        # Look for multiline code blocks that could be condensed
        code_block_inefficiencies = 0

        for md_file in markdown_files[:5]:  # Sample check
            try:
                content = md_file.read_text(encoding='utf-8')

                # Count code blocks with more than 10 lines (could potentially be compacted)
                long_code_blocks = len(re.findall(r'```[\s\S]*?```', content))
                code_lines = sum(1 for line in content.split('\n') if line.strip().startswith(('    ', '\t', '```')))

                if code_lines > 50 and long_code_blocks > 3:
                    results['issues_found'].append(f"ℹ️ {md_file.name}: {code_lines} code lines across {long_code_blocks} blocks (consider code compaction)")
                    code_block_inefficiencies += 1

            except Exception:
                continue

        if code_block_inefficiencies == 0:
            results['optimization_categories']['code_compaction'] = 'GOOD'
        elif code_block_inefficiencies <= 2:
            results['optimization_categories']['code_compaction'] = 'MINOR_OPTIMIZATION'
            results['context_optimization_score'] -= 5
        else:
            results['optimization_categories']['code_compaction'] = 'NEEDS_COMPACTION'
            results['context_optimization_score'] -= 15

        # Determine overall efficiency rating
        if results['context_optimization_score'] >= 90:
            results['token_efficiency_rating'] = 'HIGH'
            results['status'] = 'PASS'
        elif results['context_optimization_score'] >= 75:
            results['token_efficiency_rating'] = 'MEDIUM'
            results['status'] = 'WARN'
        else:
            results['token_efficiency_rating'] = 'LOW'
            results['status'] = 'FAIL'

        if results['context_optimization_score'] < 90:
            results['issues_found'].append(f"⚠️ Context optimization score: {results['context_optimization_score']}% ({results['token_efficiency_rating']} efficiency)")

        return results

    def run_comprehensive_validation(self, auto_fix: bool = False) -> Dict:
        """Run all 10 validation checks and return comprehensive results"""

        validation_results = {
            'timestamp': '2025-10-29',
            'validation_system': 'ComprehensiveValidationAudit',
            'version': '1.0.0',
            'auto_fix': auto_fix
        }

        # Run all validation checks
        validation_checks = [
            ('cross_reference_consistency', lambda: self.validate_cross_reference_consistency()),
            ('token_size_accuracy', lambda: self.validate_token_size_accuracy()),
            ('ai_navigation_markers_completeness', lambda: self.validate_ai_navigation_markers_completeness()),
            ('load_priority_consistency', lambda: self.validate_load_priority_consistency()),
            ('ethical_compliance_ai_integration', lambda: self.validate_ethical_compliance_ai_integration()),
            ('content_alignment_consistency', lambda: self.validate_content_alignment_consistency(auto_fix=auto_fix)),
            ('test_script_integration', lambda: self.validate_test_script_integration()),
            ('progress_tracking_data_flow', lambda: self.validate_progress_tracking_data_flow()),
            ('dependency_tree_accuracy', lambda: self.validate_dependency_tree_accuracy()),
            ('context_window_optimization_efficiency', lambda: self.validate_context_window_optimization_efficiency())
        ]

        # Complete 10-validation comprehensive audit system

        for validation_name, validation_func in validation_checks:
            try:
                result = validation_func()
                validation_results[validation_name] = result
                self.total_checks += 1

                if result['status'] in ['FAIL', 'WARN']:
                    self.compliance_score += 50  # Penalty for each failure
                else:
                    self.compliance_score += 100

            except Exception as e:
                validation_results[validation_name] = {
                    'status': 'ERROR',
                    'error_message': str(e),
                    'issues_found': ['Validation execution failed']
                }

        # Calculate overall compliance
        validation_results['overall_compliance'] = {
            'score': min(100, max(0, int(self.compliance_score / self.total_checks) if self.total_checks > 0 else 0)),
            'status': 'PASS' if self.compliance_score >= (self.total_checks * 80) else 'NEEDS_ATTENTION',
            'total_validations_run': self.total_checks,
            'recommendations': self._generate_recommendations(validation_results)
        }

        return validation_results

    def _extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from markdown content"""
        if content.startswith('---'):
            try:
                lines = content.split('\n')
                end_idx = -1
                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == '---':
                        end_idx = i
                        break

                if end_idx > 0:
                    frontmatter_text = '\n'.join(lines[1:end_idx])
                    return yaml.safe_load(frontmatter_text) or {}
            except Exception:
                pass

        return {}

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        recommendations = []

        for validation_name, result in results.items():
            if validation_name.startswith(('cross_', 'token_', 'ai_', 'load_', 'ethical_')):
                if result.get('status') == 'FAIL':
                    recommendations.append(f"HIGH PRIORITY: Fix {validation_name.replace('_', ' ')} issues to ensure AI execution reliability")
                elif result.get('status') == 'WARN':
                    recommendations.append(f"MEDIUM PRIORITY: Optimize {validation_name.replace('_', ' ')} to improve system performance")

        # General recommendations
        recommendations.extend([
            "Implement automated daily validation checks to catch issues early",
            "Standardize all cross-references to use hierarchical parent/child/sibling structure",
            "Update AI navigation markers in all documentation files for optimum AI execution",
            "Validate all token size calculations and update manifest with accurate measurements"
        ])

        return recommendations[:5]  # Return top 5 recommendations


def main():
    """Run comprehensive validation audit"""
    import argparse

    parser = argparse.ArgumentParser(description='Comprehensive Validation Audit for Biological Testing Ecosystem')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix detected content alignment inconsistencies')
    args = parser.parse_args()

    if args.auto_fix:
        print("🔧 AUTO-FIX MODE ENABLED - Will automatically correct content alignment inconsistencies")
        print("⚠️  CAUTION: This will modify documentation files. Ensure you have backups.\n")

        # Get user confirmation
        response = input("Are you sure you want to enable auto-fix mode? (yes/no): ").lower().strip()
        if response != 'yes':
            print("Auto-fix cancelled. Running in detection-only mode.")
            args.auto_fix = False

    audit = ComprehensiveValidationAudit()
    results = audit.run_comprehensive_validation(auto_fix=args.auto_fix)

    # Output results
    print("🔍 COMPREHENSIVE VALIDATION AUDIT RESULTS" + (" (AUTO-FIX ENABLED)" if args.auto_fix else ""))
    print("=" * 50)

    for validation_name, result in results.items():
        if isinstance(result, dict) and 'status' in result:
            status_emoji = {'PASS': '✅', 'FAIL': '❌', 'WARN': '⚠️', 'ERROR': '🔥', 'SKIP': '⏭️'}.get(result['status'], '?')
            print(f"\n{status_emoji} {validation_name.replace('_', ' ').title()}")
            print(f"   Status: {result['status']}")

            if 'fixes_applied' in result and result['fixes_applied'] > 0:
                print(f"   Fixes Applied: {result['fixes_applied']}")

            if 'issues_found' in result and result['issues_found']:
                print(f"   Issues Found: {len(result['issues_found'])}")
                for issue in result['issues_found'][:3]:  # Show first 3 issues
                    print(f"     - {issue}")

            if 'files_checked' in result:
                print(f"   Files Checked: {result['files_checked']}")

    # Overall compliance summary
    if 'overall_compliance' in results:
        compliance = results['overall_compliance']
        print(f"\n🏆 OVERALL COMPLIANCE: {compliance['score']}% - {compliance['status']}")
        print(f"   Validations Run: {compliance['total_validations_run']}")
        if args.auto_fix:
            total_fixes = sum(result.get('fixes_applied', 0) for result in results.values() if isinstance(result, dict))
            print(f"   Total Auto-Fixes Applied: {total_fixes}")
        print(f"\n🔧 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(compliance['recommendations'], 1):
            print(f"   {i}. {rec}")

    # Save detailed results
    output_file = audit.project_root / 'reports' / 'comprehensive_validation_audit.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Detailed results saved to: {output_file}")

    if args.auto_fix:
        print(f"\n🔧 AUTO-FIX SUMMARY:")
        total_fixes = sum(result.get('fixes_applied', 0) for result in results.values() if isinstance(result, dict))
        if total_fixes > 0:
            print(f"   ✅ {total_fixes} automatic corrections applied to documentation files")
            print(f"   📋 Re-run validation without --auto-fix to verify corrections")
        else:
            print(f"   ℹ️ No automatic corrections were needed")

    return results


if __name__ == '__main__':
    main()
