#!/usr/bin/env python3
"""
Automatic Print to Logging Converter for JTP Biological Organism

This script systematically converts all print() statements to proper logging calls
across the entire codebase.
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Tuple

# Setup converter logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
converter_logger = logging.getLogger(__name__)

class PrintToLoggingConverter:
    """Systematic print() to logging conversion tool"""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.conversion_stats = {
            'files_processed': 0,
            'print_statements_found': 0,
            'print_statements_converted': 0,
            'files_modified': 0,
            'errors': 0
        }

        # Logging level patterns to detect intent
        self.level_patterns = {
            'error': re.compile(r'print\([^)]*error[^)]*\)', re.IGNORECASE),
            'warning': re.compile(r'print\([^)]*(warn|⚠️|caution|alert)[^)]*\)', re.IGNORECASE | re.UNICODE),
            'debug': re.compile(r'print\([^)]*(debug|trace|step|iteration)[^)]*\)', re.IGNORECASE),
            'critical': re.compile(r'print\([^)]*(critical|emergency|fatal|crash)[^)]*\)', re.IGNORECASE),
        }

    def scan_for_print_statements(self, file_path: Path) -> List[Tuple[int, str]]:
        """Scan a file for print statements and return line numbers with content"""
        prints = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    # Find print statements (handle indentation and various formats)
                    print_match = re.search(r'^(.*?)print\s*\(', line)
                    if print_match:
                        prints.append((i, line.rstrip()))
        except Exception as e:
            converter_logger.error(f"Error reading {file_path}: {e}")
            self.conversion_stats['errors'] += 1

        self.conversion_stats['print_statements_found'] += len(prints)
        return prints

    def determine_log_level(self, print_statement: str) -> str:
        """Determine appropriate logging level from print statement content"""
        for level, pattern in self.level_patterns.items():
            if pattern.search(print_statement):
                return level.upper()

        # Default to INFO for generic prints
        return 'INFO'

    def convert_print_to_logging(self, print_statement: str) -> str:
        """Convert a print statement to appropriate logging call"""
        # Extract the print arguments
        print_match = re.search(r'print\s*\((.*?)\)\s*$', print_statement.strip())
        if not print_match:
            return print_statement  # Return unchanged if can't parse

        content = print_match.group(1).strip()

        # Determine logging level
        log_level = self.determine_log_level(print_statement)

        # Convert to logging call
        converted = f"logger.{log_level.lower()}({content})"

        converter_logger.debug(f"Converted: '{print_statement.strip()}' → '{converted}'")
        return converted

    def add_logging_import(self, content: str) -> str:
        """Add logging import if not already present"""
        lines = content.split('\n')

        # Check if logging is already imported
        has_logging_import = any('import logging' in line for line in lines)
        has_logger_declaration = any('logger = logging.getLogger' in line for line in lines)

        if not has_logging_import:
            # Find first import statement or add at top
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_pos = i + 1
                    break

            lines.insert(insert_pos, 'import logging')
            converter_logger.debug("Added 'import logging' to file")

        if not has_logger_declaration:
            # Find where to add logger declaration (after imports, before first function/class)
            insert_pos = 0
            for i, line in enumerate(lines):
                if not line.strip() or line.strip().startswith(('import ', 'from ', '"""', "'''", '#')):
                    continue
                # Stop at first real code (function def, class def, or assignment)
                if any(line.strip().startswith(keyword) for keyword in ['def ', 'class ', 'if __name__']):
                    break
                insert_pos = i + 1

            # Add logger declaration
            lines.insert(insert_pos, "\n# Get logger for this module\nlogger = logging.getLogger(__name__)")
            converter_logger.debug("Added logger declaration to file")

        return '\n'.join(lines)

    def process_file(self, file_path: Path) -> bool:
        """Process a single file for print to logging conversion"""
        converter_logger.info(f"Processing file: {file_path}")

        # Skip if no print statements
        print_statements = self.scan_for_print_statements(file_path)
        if not print_statements:
            converter_logger.debug(f"No print statements found in {file_path}")
            return False

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            converter_logger.error(f"Error reading {file_path}: {e}")
            self.conversion_stats['errors'] += 1
            return False

        # Add logging import/declaration if needed
        content = self.add_logging_import(content)

        # Process each print statement
        modified = False
        lines = content.split('\n')

        for line_num, line_content in print_statements:
            if line_num <= len(lines):
                converted_line = self.convert_print_to_logging(line_content)

                # Find the exact line in content and replace it
                original_line = lines[line_num - 1]
                if 'print(' in original_line:
                    lines[line_num - 1] = converted_line
                    self.conversion_stats['print_statements_converted'] += 1
                    modified = True
                    converter_logger.debug(f"Converted line {line_num} in {file_path}")

        # Write back if modified
        if modified:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                self.conversion_stats['files_modified'] += 1
                converter_logger.info(f"Modified file: {file_path}")
                return True
            except Exception as e:
                converter_logger.error(f"Error writing {file_path}: {e}")
                self.conversion_stats['errors'] += 1
                return False

        return False

    def process_all_files(self) -> None:
        """Process all Python files in the codebase"""
        print("🧬 STARTING SYSTEMATIC PRINT TO LOGGING CONVERSION")
        print("=" * 70)

        python_files = list(self.root_path.rglob('*.py'))

        total_files = len(python_files)
        print(f"📊 Found {total_files} Python files to process")

        processed = 0
        for file_path in python_files:
            # Skip the converter script itself
            if file_path.name == 'convert_prints_to_logging.py':
                continue

            processed += 1
            self.process_file(file_path)

            # Progress indicator
            if processed % 50 == 0:
                print(f"📈 Progress: {processed}/{total_files} files processed")

        self.conversion_stats['files_processed'] = processed

        # Final report
        print("\n" + "=" * 70)
        print("📊 LOGGING CONVERSION SUMMARY")
        print("=" * 70)
        print(f"✅ Files processed: {self.conversion_stats['files_processed']}")
        print(f"🔍 Print statements found: {self.conversion_stats['print_statements_found']}")
        print(f"🔄 Print statements converted: {self.conversion_stats['print_statements_converted']}")
        print(f"📝 Files modified: {self.conversion_stats['files_modified']}")
        print(f"❌ Errors encountered: {self.conversion_stats['errors']}")

        success_rate = (self.conversion_stats['print_statements_converted'] /
                       max(self.conversion_stats['print_statements_found'], 1) * 100)

        print(".1f")
        if self.conversion_stats['print_statements_converted'] > 0:
            print("✅ LOGGING CONVERSION COMPLETED SUCCESSFULLY")
            print(f"   All {self.conversion_stats['files_modified']} modified files now use structured logging")
        else:
            print("ℹ️  No print statements were converted (may already be converted)")


def main():
    import sys

    if len(sys.argv) < 2:
        root_path = Path.cwd() / 'src'
        print(f"Using default path: {root_path}")
    else:
        root_path = Path(sys.argv[1])

    if not root_path.exists():
        print(f"❌ Path does not exist: {root_path}")
        sys.exit(1)

    converter = PrintToLoggingConverter(root_path)
    converter.process_all_files()


if __name__ == "__main__":
    main()
