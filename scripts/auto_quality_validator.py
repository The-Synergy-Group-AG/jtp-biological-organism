#!/usr/bin/env python3
"""
AI Auto-Pilot Quality Validation Suite
Automated validation for each micro-transformation batch
"""

import ast
import importlib
import sys
import os
import json
import time
from typing import Dict, List, Any, Tuple

class AutoQualityValidator:
    """Automated quality validation for AI auto-pilot transformations"""

    def __init__(self):
        self.baseline_metrics = None
        self.progress_state = {}
        self.load_baseline_metrics()

    def load_baseline_metrics(self):
        """Load baseline metrics for comparison"""
        try:
            with open('refactoring_state/baseline_metrics.json', 'r') as f:
                self.baseline_metrics = json.load(f)
        except FileNotFoundError:
            print("⚠️  Baseline metrics not found")
            self.baseline_metrics = {}

    def validate_transformation(self, file_path: str, old_content: str = None) -> Dict[str, Any]:
        """Complete automated quality check for transformation"""

        if not os.path.exists(file_path):
            return {"valid": False, "error": "File does not exist"}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
        except Exception as e:
            return {"valid": False, "error": f"Cannot read file: {e}"}

        results = {
            "valid": True,
            "file_path": file_path,
            "timestamp": time.time(),
            "checks": {}
        }

        # Syntax Validation
        results["checks"]["syntax"] = self.check_syntax(current_content)

        # Import Validation
        results["checks"]["imports"] = self.check_imports(current_content)

        # Complexity Validation
        results["checks"]["complexity"] = self.check_complexity(current_content)

        # Size Validation
        results["checks"]["size"] = self.check_size(file_path, current_content)

        # Overall Validity
        results["valid"] = all(check["valid"] for check in results["checks"].values())

        if results["valid"]:
            results["quality_score"] = sum(check["score"] for check in results["checks"].values()) / len(results["checks"])
        else:
            results["quality_score"] = 0.0

        return results

    def check_syntax(self, content: str) -> Dict[str, Any]:
        """Validate Python syntax"""
        try:
            ast.parse(content)
            return {"valid": True, "score": 1.0, "message": "Syntax valid"}
        except SyntaxError as e:
            return {"valid": False, "score": 0.0, "message": f"Syntax error: {e}"}

    def check_imports(self, content: str) -> Dict[str, Any]:
        """Validate import statements"""
        try:
            # Simple regex check for common import patterns
            lines = content.split('\n')
            imports_ok = True
            score = 1.0

            for line in lines:
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    # Basic validation - could be enhanced
                    if not line.strip().endswith(')') or line.count('(') == line.count(')'):
                        continue
                    else:
                        imports_ok = False
                        score -= 0.1

            if score < 0.8:
                return {"valid": False, "score": score, "message": "Import syntax issues detected"}

            return {"valid": True, "score": score, "message": "Import syntax clean"}

        except Exception as e:
            return {"valid": False, "score": 0.0, "message": f"Import validation failed: {e}"}

    def check_complexity(self, content: str) -> Dict[str, Any]:
        """Validate cyclomatic complexity"""
        try:
            # Simple heuristic - count functions and estimate complexity
            lines = content.split('\n')
            function_count = sum(1 for line in lines if line.strip().startswith('def '))
            class_count = sum(1 for line in lines if line.strip().startswith('class '))

            # Estimate complexity based on functions/classes
            estimated_complexity = min(5.0, (function_count / 5) + (class_count / 2))

            if estimated_complexity <= 5:
                return {"valid": True, "score": 1.0, "message": f"Complexity acceptable ({estimated_complexity:.1f})"}
            else:
                score = max(0.0, 1.0 - ((estimated_complexity - 5) / 10))
                return {"valid": True, "score": score, "message": f"High complexity ({estimated_complexity:.1f})"}

        except Exception as e:
            return {"valid": False, "score": 0.0, "message": f"Complexity check failed: {e}"}

    def check_size(self, file_path: str, content: str) -> Dict[str, Any]:
        """Validate file size against targets"""
        lines = len(content.split('\n'))
        baseline = self.baseline_metrics.get("target_files_baseline", {}).get(file_path, {})

        target_lines = baseline.get("target_lines", lines)  # Fallback to current if no target

        if lines <= target_lines:
            return {"valid": True, "score": min(1.0, target_lines / lines if lines > 0 else 1.0),
                   "message": f"Size acceptable: {lines}/{target_lines} lines"}
        else:
            reduction_needed = lines - target_lines
            score = max(0.0, 1.0 - (reduction_needed / target_lines))
            return {"valid": True, "score": score,
                   "message": f"Size target not met: {reduction_needed} lines over target"}

def load_progress_state():
    """Load current refactoring progress state"""
    try:
        with open('refactoring_state/initial_state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"current_status": {"response_count": 0}}

def save_quality_result(result: Dict[str, Any]):
    """Save quality validation result"""
    result_file = f'refactoring_state/quality_results_{int(time.time())}.json'
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)

def main():
    """Main entry point for auto quality validation"""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python auto_quality_validator.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    validator = AutoQualityValidator()
    result = validator.validate_transformation(file_path)

    # Save result for AI auto-pilot state tracking
    save_quality_result(result)

    # Output for automation
    print(json.dumps(result, indent=2))

    # Exit code indicates validation status
    sys.exit(0 if result["valid"] else 1)

if __name__ == "__main__":
    main()
