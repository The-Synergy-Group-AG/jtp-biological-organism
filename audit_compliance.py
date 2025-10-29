#!/usr/bin/env python3
"""
Automated Documentation Compliance Audit System

Performs scheduled compliance audits with sampling, trend analysis, and reporting.
Supports weekly and monthly audit modes with varying sampling rates.

Usage:
    # Weekly audit (10% random sampling)
    python audit_compliance.py --weekly

    # Monthly audit (25% comprehensive sampling)
    python audit_compliance.py --monthly

    # Manual custom audit
    python audit_compliance.py --sample-rate 0.05 --output custom_audit_report.md
"""

import os
import random
import datetime
import json
from pathlib import Path
from typing import Dict, List, Tuple
import yaml
import argparse

class ComplianceAuditor:
    def __init__(self, docs_path="docs", sample_rate=0.1, verbose=False):
        self.docs_path = Path(docs_path)
        self.sample_rate = sample_rate
        self.verbose = verbose
        self.report_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "audit_type": "manual",
            "sample_rate": sample_rate,
            "documents_analyzed": 0,
            "compliance_violations": [],
            "ethical_score_distribution": {
                "excellent": 0,  # 91-100%
                "good": 0,       # 75-90%
                "marginal": 0,   # 50-74%
                "poor": 0        # <50%
            },
            "trend_analysis": {},
            "recommendations": []
        }

    def log(self, message):
        if self.verbose:
            print(f"[AUDIT] {message}")

    def find_all_docs(self) -> List[Path]:
        """Find all markdown documentation files"""
        return list(self.docs_path.rglob('*.md'))

    def sample_documents(self, docs: List[Path]) -> List[Path]:
        """Sample documents based on configured rate"""
        if self.sample_rate >= 1.0:
            return docs  # Full audit

        sample_size = max(1, int(len(docs) * self.sample_rate))
        return random.sample(docs, sample_size)

    def score_to_category(self, score: float) -> str:
        """Categorize ethical scores"""
        if score >= 91:
            return "excellent"
        elif score >= 75:
            return "good"
        elif score >= 50:
            return "marginal"
        else:
            return "poor"

    def audit_document(self, doc_path: Path) -> Dict:
        """Comprehensive audit of single document"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "file": str(doc_path),
                "status": "error",
                "error": str(e),
                "ethical_score": None
            }

        # Extract ethical score from frontmatter
        score_match = ""
        frontmatter_match = os.popen(f'grep -P "^ethical_score:" -A 1 {doc_path}').read().strip()
        if frontmatter_match:
            # Try to extract percentage
            score_match = os.popen(f'grep -Po "\d+(?=%| score)" {doc_path} | head -1').read().strip()

        ethical_score = int(score_match) if score_match and score_match.isdigit() else 0

        violations = []

        # Basic compliance checks
        if ethical_score < 75:
            violations.append(f"Ethical score {ethical_score}% below minimum 75%")

        if not content:
            violations.append("Document is empty")

        # Check for required sections
        required_sections = ["## Ethical Score", "## Status", "## Authors"]
        for section in required_sections:
            if section not in content:
                violations.append(f"Missing required section: {section}")

        # Update score distribution
        category = self.score_to_category(ethical_score)
        self.report_data["ethical_score_distribution"][category] += 1

        return {
            "file": str(doc_path),
            "ethical_score": ethical_score,
            "violations": violations,
            "word_count": len(content.split()),
            "line_count": len(content.split('\n')),
            "last_modified": datetime.datetime.fromtimestamp(doc_path.stat().st_mtime).isoformat()
        }

    def load_historical_data(self) -> List[Dict]:
        """Load previous audit results for trend analysis"""
        history_file = Path("reports/compliance_history.json")
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_audit_data(self, audit_results: List[Dict]):
        """Save current audit data for future trend analysis"""
        history_file = Path("reports")
        history_file.mkdir(exist_ok=True)
        history_file = history_file / "compliance_history.json"

        historical_data = self.load_historical_data()

        # Add current audit
        current_audit = {
            "timestamp": self.report_data["timestamp"],
            "audit_type": self.report_data["audit_type"],
            "sample_rate": self.sample_rate,
            "results": audit_results[:10],  # Only keep summary of recent audits
            "avg_score": sum(r.get("ethical_score", 0) for r in audit_results) / len(audit_results) if audit_results else 0
        }

        historical_data.append(current_audit)
        # Keep only last 12 months
        historical_data = historical_data[-52:]  # Assuming weekly audits

        with open(history_file, 'w') as f:
            json.dump(historical_data, f, indent=2)

    def analyze_trends(self) -> Dict:
        """Analyze trends from historical data"""
        historical = self.load_historical_data()
        if len(historical) < 2:
            return {"note": "Insufficient data for trend analysis"}

        # Calculate trends
        recent_audits = historical[-4:]  # Last month if weekly audits
        if recent_audits:
            scores = [a.get("avg_score", 0) for a in recent_audits]
            avg_recent = sum(scores) / len(scores) if scores else 0

            trend = {
                "average_score_last_period": avg_recent,
                "score_trend": "stable",
                "data_points": len(historical)
           }

            # Simple trend detection
            if len(scores) > 1:
                if scores[-1] > scores[0] + 2:
                    trend["score_trend"] = "improving"
                elif scores[-1] < scores[0] - 2:
                    trend["score_trend"] = "declining"

            return trend

        return {"note": "No recent data available"}

    def generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on audit results"""
        recommendations = []

        violation_count = sum(1 for r in results if r.get("violations"))
        if violation_count > len(results) * 0.1:
            recommendations.append(f"⚠️ High violation rate ({violation_count}/{len(results)}). Consider author training.")

        avg_score = sum(r.get("ethical_score", 0) for r in results) / len(results) if results else 0
        if avg_score < 85:
            recommendations.append(f"⚠️ Average score ({avg_score:.0f}) below target. Priority improvements needed.")
        elif avg_score > 95:
            recommendations.append("🎉 Excellent compliance maintained. Consider documenting best practices.")

        low_score_docs = [r for r in results if (r.get("ethical_score") or 0) < 80]
        if low_score_docs:
            doc_names = [Path(r["file"]).stem for r in low_score_docs[:3]]
            recommendations.append(f"📝 Priority review needed for: {', '.join(doc_names)}")

        return recommendations

    def run_weekly_audit(self):
        """Run weekly compliance audit (10% sampling)"""
        self.report_data["audit_type"] = "weekly"
        self.sample_rate = 0.1
        return self.run_audit()

    def run_monthly_audit(self):
        """Run monthly comprehensive audit (25% sampling)"""
        self.report_data["audit_type"] = "monthly"
        self.sample_rate = 0.25
        return self.run_audit()

    def run_audit(self) -> Dict:
        """Execute the compliance audit"""
        print(f"\n🔍 Running {self.report_data['audit_type'].upper()} Compliance Audit")
        print("=" * 60)
        print(f"📊 Sample Rate: {self.sample_rate*100:.0f}%")
        print(f"⏰ Timestamp: {self.report_data['timestamp']}")

        # Find and sample documents
        all_docs = self.find_all_docs()
        sampled_docs = self.sample_documents(all_docs)

        print(f"📑 Total Documents Found: {len(all_docs)}")
        print(f"🎯 Documents in Sample: {len(sampled_docs)}")

        # Audit sampled documents
        audit_results = []
        for doc in sampled_docs:
            self.log(f"Auditing {doc.name}")
            result = self.audit_document(doc)
            audit_results.append(result)

            if result["violations"]:
                self.report_data["compliance_violations"].append(result)

        # Analysis
        self.report_data["trend_analysis"] = self.analyze_trends()
        self.report_data["recommendations"] = self.generate_recommendations(audit_results)

        # Save results for future trend analysis
        self.save_audit_data(audit_results)

        # Update counts
        self.report_data["documents_analyzed"] = len(sampled_docs)

        return self.report_data

    def generate_report_markdown(self, output_file: Path) -> str:
        """Generate markdown audit report"""
        r = self.report_data
        dist = r["ethical_score_distribution"]

        violations_text = "\n".join(f"- **{v['file']}**: {', '.join(v['violations'])}" for v in r["compliance_violations"][:10]) \
                         + ("\n- ... (showing first 10)" if len(r["compliance_violations"]) > 10 else "")

        report = f"""# 📋 {r["audit_type"].title()} Compliance Audit Report

**Audit Timestamp:** {r["timestamp"]}
**Sample Rate:** {r["sample_rate"]*100:.0f}%
**Documents Analyzed:** {r["documents_analyzed"]}

## 📊 Compliance Overview

| Metric | Value | Status |
|--------|-------|--------|
| **Sample Rate** | {r["sample_rate"]*100:.0f}% | ✅ |
| **Documents Analyzed** | {r["documents_analyzed"]} | ✅ |
| **Violations Found** | {len(r["compliance_violations"])} | """

        report += '❌' if r["compliance_violations"] else '✅'
        report += f""" |

## 📈 Ethical Score Distribution

- **Excellent (91-100%)**: {dist["excellent"]}
- **Good (75-90%)**: {dist["good"]}
- **Marginal (50-74%)**: {dist["marginal"]}
- **Poor (<50%)**: {dist["poor"]}

## 🎯 Trend Analysis

{json.dumps(r["trend_analysis"], indent=2) if r.get("trend_analysis") else "No historical data available"}

## ⚠️ Compliance Violations

{violations_text}

## 💡 Recommendations

"""
        for rec in r["recommendations"]:
            report += f"- {rec}\n"

        report += """
---
*Generated by Automated Compliance Audit System*
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

        return report

def main():
    parser = argparse.ArgumentParser(description='Automated Documentation Compliance Auditor')
    parser.add_argument('--weekly', action='store_true', help='Run weekly audit (10% sampling)')
    parser.add_argument('--monthly', action='store_true', help='Run monthly audit (25% sampling)')
    parser.add_argument('--sample-rate', type=float, default=0.1, help='Custom sample rate (0.0-1.0)')
    parser.add_argument('--output', type=Path, default=Path('compliance_audit_report.md'),
                       help='Output report file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Set audit type
    if args.weekly:
        auditor = ComplianceAuditor(sample_rate=0.1, verbose=args.verbose)
        auditor.run_weekly_audit()
    elif args.monthly:
        auditor = ComplianceAuditor(sample_rate=0.25, verbose=args.verbose)
        auditor.run_monthly_audit()
    else:
        auditor = ComplianceAuditor(sample_rate=args.sample_rate, verbose=args.verbose)
        auditor.run_audit()

    # Generate and save report
    report_content = auditor.generate_report_markdown(args.output)
    print(f"\n📄 Report saved to: {args.output}")

    # Print summary
    violations = len(auditor.report_data["compliance_violations"])
    if violations == 0:
        print("🎉 FULL COMPLIANCE ACHIEVED - No violations found!")
    else:
        print(f"⚠️ {violations} compliance violations detected. See report for details.")

if __name__ == '__main__':
    main()
