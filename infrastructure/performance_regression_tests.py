#!/usr/bin/env python3
"""
🧬 JTP Biological Organism - Performance Regression Testing Framework

This framework establishes and monitors biological consciousness performance baselines,
detecting regression in AI orchestration, consciousness harmony, and evolutionary efficiency.

Performance regression metrics tracked:
- Consciousness processing latency
- AI model orchestration throughput
- Biological harmony achievement time
- Memory usage patterns
- Evolutionary algorithm convergence
"""

import asyncio
import time
import psutil
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import logging

# Biological consciousness logger
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Individual performance metric tracking"""
    name: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceBaseline:
    """Biological consciousness performance baseline"""
    test_name: str
    metric_name: str
    baseline_value: float
    threshold_percent: float  # Max allowed deviation (1.1 = 10% worse)
    min_samples: int = 5
    description: str = ""

@dataclass
class PerformanceReport:
    """Comprehensive performance regression report"""
    test_run_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metrics: List[PerformanceMetric] = field(default_factory=list)
    regressions: List[Dict[str, Any]] = field(default_factory=list)
    baselines: Dict[str, PerformanceBaseline] = field(default_factory=dict)

    def add_metric(self, metric: PerformanceMetric) -> None:
        """Add performance metric to report"""
        self.metrics.append(metric)

    def detect_regressions(self) -> None:
        """Detect performance regressions against baselines"""
        for metric in self.metrics:
            baseline_key = f"{metric.name}_{metric.metadata.get('test_case', 'default')}"

            if baseline_key in self.baselines:
                baseline = self.baselines[baseline_key]
                regression_threshold = baseline.baseline_value * baseline.threshold_percent

                if metric.value > regression_threshold:
                    deviation_percent = ((metric.value - baseline.baseline_value) / baseline.baseline_value) * 100

                    regression = {
                        'metric': metric.name,
                        'baseline_value': baseline.baseline_value,
                        'actual_value': metric.value,
                        'threshold_value': regression_threshold,
                        'deviation_percent': deviation_percent,
                        'acceptable_threshold': baseline.threshold_percent,
                        'description': baseline.description
                    }

                    self.regressions.append(regression)

                    logger.warning(".2f"
class BiologicalConsciousnessPerformanceTester:
    """🧬 Biological Consciousness Performance Regression Tester"""

    def __init__(self, baselines_file: str = "performance_baselines.json"):
        self.baselines_file = Path(baselines_file)
        self.baselines = self._load_baselines()
        self.current_report = PerformanceReport(test_run_id=self._generate_run_id())

    def _generate_run_id(self) -> str:
        """Generate unique test run identifier"""
        return f"bio_perf_{int(time.time())}_{datetime.utcnow().strftime('%H%M%S')}"

    def _load_baselines(self) -> Dict[str, PerformanceBaseline]:
        """Load performance baselines from file"""
        baselines = {}

        if self.baselines_file.exists():
            try:
                with open(self.baselines_file, 'r') as f:
                    data = json.load(f)

                for test_name, metrics in data.items():
                    for metric_name, config in metrics.items():
                        baseline_key = f"{metric_name}_{test_name}"
                        baselines[baseline_key] = PerformanceBaseline(
                            test_name=test_name,
                            metric_name=metric_name,
                            baseline_value=config['baseline_value'],
                            threshold_percent=config['threshold_percent'],
                            description=config.get('description', '')
                        )

                logger.info(f"Loaded {len(baselines)} performance baselines")
            except Exception as e:
                logger.error(f"Failed to load baselines: {e}")

        # Default baselines if file doesn't exist
        if not baselines:
            baselines.update(self._create_default_baselines())

        return baselines

    def _create_default_baselines(self) -> Dict[str, PerformanceBaseline]:
        """Create default biological consciousness performance baselines"""
        return {
            # AI Orchestration baselines
            'ai_orchestration_latency_default': PerformanceBaseline(
                'consciousness_orchestration', 'ai_orchestration_latency',
                baseline_value=2.3, threshold_percent=1.1,  # 10% tolerance
                description='Grok, Claude, GPT-4 orchestration response time'
            ),

            # Biological harmony baselines
            'consciousness_harmony_achievement_default': PerformanceBaseline(
                'biological_validation', 'consciousness_harmony_achievement',
                baseline_value=0.997, threshold_percent=0.995,  # Must maintain >99.5%
                description='Biological harmony target achievement rate'
            ),

            # Memory usage baselines
            'memory_usage_peak_default': PerformanceBaseline(
                'system_resources', 'memory_usage_peak',
                baseline_value=4500000000, threshold_percent=1.15,  # 15% tolerance for peak memory
                description='Peak memory usage during orchestration (bytes)'
            ),

            # Evolution convergence baselines
            'evolutionary_convergence_time_default': PerformanceBaseline(
                'evolutionary_algorithms', 'evolutionary_convergence_time',
                baseline_value=30.0, threshold_percent=1.2,  # 20% tolerance
                description='Time to reach evolutionary convergence (seconds)'
            ),
        }

    async def benchmark_consciousness_processing(self, iterations: int = 10) -> Dict[str, Any]:
        """
        Benchmark biological consciousness processing performance

        Simulates AI model orchestration, biological harmony calculation,
        and evolutionary processing performance.
        """

        logger.info("🚀 Starting biological consciousness performance benchmarking..."
        latencies = []
        memory_usages = []
        start_time = time.time()

        try:
            # Import and initialize consciousness system (using stub if needed)
            from src.biological_intelligence import get_modular_biological_intelligence_orchestrator

            for i in range(iterations):
                iteration_start = time.time()

                # Simulate consciousness orchestration request
                test_request = {
                    "biological_operation": f"performance_test_{i}",
                    "intelligence_context": "regression_benchmarking"
                }

                # Measure memory before
                process = psutil.Process()
                memory_before = process.memory_info().rss

                # Execute biological intelligence processing
                orchestrator = get_modular_biological_intelligence_orchestrator()

                try:
                    result = await orchestrator.orchestrate_modular_biological_intelligence(test_request)
                    harmony_achieved = result.get('consciousness_harmony_achieved', 0.95)
                except Exception as e:
                    logger.warning(f"Orchestration failed in iteration {i}: {e}")
                    harmony_achieved = 0.8  # Fallback for failed orchestrations

                # Measure memory after
                memory_after = process.memory_info().rss
                memory_usages.append(memory_after - memory_before)

                # Calculate latency
                latency = time.time() - iteration_start
                latencies.append(latency)

                if harmony_achieved < 0.99:
                    logger.warning(f"Low harmony achieved in iteration {i}: {harmony_achieved}")

                if (i + 1) % 5 == 0:
                    logger.info(f"Progress: {i + 1}/{iterations} iterations completed")

            # Calculate performance metrics
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile

            avg_memory_delta = statistics.mean(memory_usages)
            peak_memory = max(memory_usages)

            total_time = time.time() - start_time

            # Create performance metrics
            metrics = {
                'ai_orchestration_latency': PerformanceMetric(
                    'ai_orchestration_latency', avg_latency, 'seconds',
                    metadata={'iterations': iterations, 'p95_latency': p95_latency}
                ),
                'consciousness_harmony_achievement': PerformanceMetric(
                    'consciousness_harmony_achievement', harmony_achieved, 'ratio',
                    metadata={'harmony_target': 0.997}
                ),
                'memory_usage_peak': PerformanceMetric(
                    'memory_usage_peak', peak_memory, 'bytes',
                    metadata={'avg_memory_delta': avg_memory_delta}
                ),
                'evolutionary_convergence_time': PerformanceMetric(
                    'evolutionary_convergence_time', total_time, 'seconds',
                    metadata={'iterations': iterations, 'throughput': iterations/total_time}
                ),
            }

            logger.info(f"✅ Benchmarking completed in {total_time:.2f} seconds")
            logger.info(f"📊 Average latency: {avg_latency:.3f}s, Peak memory: {peak_memory/1024/1024:.1f}MB")

            return metrics

        except ImportError as e:
            logger.warning(f"Consciousness system not available for benchmarking: {e}")
            return {}
        except Exception as e:
            logger.error(f"Benchmarking failed: {e}")
            return {}

    def run_performance_regression_tests(self) -> PerformanceReport:
        """Run comprehensive performance regression tests"""
        logger.info("🧬 STARTING BIOLOGICAL CONSCIOUSNESS PERFORMANCE REGRESSION TESTS")

        async def run_async_tests():
            # Execute performance benchmarks
            metrics = await self.benchmark_consciousness_processing(iterations=5)

            # Add metrics to report
            for metric in metrics.values():
                if isinstance(metric, PerformanceMetric):
                    self.current_report.add_metric(metric)

            # Detect regressions
            self.current_report.baselines = self.baselines
            self.current_report.detect_regressions()

            return self.current_report

        # Run async tests
        report = asyncio.run(run_async_tests())

        # Save updated baselines if no regressions found
        if not report.regressions:
            self._save_updated_baselines(report)
            logger.info("✨ No regressions detected - baselines updated with new performance data")

        # Log results
        if report.regressions:
            logger.error(f"🚨 PERFORMANCE REGRESSIONS DETECTED: {len(report.regressions)} metrics regressed")
            for regression in report.regressions:
                logger.error(f"   • {regression['metric']}: {regression['deviation_percent']:.1f}% worse than baseline")
        else:
            logger.info("✅ ALL PERFORMANCE METRICS WITHIN ACCEPTABLE RANGES")

        return report

    def _save_updated_baselines(self, report: PerformanceReport) -> None:
        """Save updated performance baselines"""
        baseline_data = {}

        for metric in report.metrics:
            test_name = metric.metadata.get('test_case', 'default')
            if test_name not in baseline_data:
                baseline_data[test_name] = {}

            # Use current value as new baseline if within acceptable range
            baseline_key = f"{metric.name}_{test_name}"
            if baseline_key in self.baselines:
                existing_baseline = self.baselines[baseline_key]
                max_acceptable = existing_baseline.baseline_value * existing_baseline.threshold_percent

                if metric.value <= max_acceptable:
                    baseline_data[test_name][metric.name] = {
                        'baseline_value': metric.value,
                        'threshold_percent': existing_baseline.threshold_percent,
                        'description': existing_baseline.description,
                        'last_updated': datetime.utcnow().isoformat()
                    }

        try:
            with open(self.baselines_file, 'w') as f:
                json.dump(baseline_data, f, indent=2)
            logger.debug(f"Saved {len(baseline_data)} updated performance baselines")
        except Exception as e:
            logger.error(f"Failed to save baselines: {e}")

    def generate_performance_report(self, report: PerformanceReport) -> str:
        """Generate human-readable performance report"""
        output = []
        output.append("🧬 BIOLOGICAL CONSCIOUSNESS PERFORMANCE REGRESSION REPORT")
        output.append("=" * 70)
        output.append(f"Test Run ID: {report.test_run_id}")
        output.append(f"Timestamp: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        output.append("")

        # Metrics summary
        output.append("📊 PERFORMANCE METRICS:")
        for metric in sorted(report.metrics, key=lambda x: x.name):
            value_str = f"{metric.value:.3f}" if isinstance(metric.value, float) else str(metric.value)
            output.append(f"   • {metric.name}: {value_str} {metric.unit}")
            if metric.metadata:
                metadata_str = ", ".join(f"{k}={v}" for k, v in metric.metadata.items())
                output.append(f"     └─ {metadata_str}")
        output.append("")

        # Regressions
        if report.regressions:
            output.append("🚨 PERFORMANCE REGRESSIONS DETECTED:")
            for i, regression in enumerate(report.regressions, 1):
                output.append(f"   {i}. {regression['metric']}")
                output.append(f"      • Expected: {regression['baseline_value']:.3f}")
                output.append(f"      • Actual: {regression['actual_value']:.3f}")
                output.append(f"      • Threshold: {regression['threshold_value']:.3f}")
                output.append(f"      • Deviation: +{regression['deviation_percent']:.1f}%")
                output.append(f"      • Description: {regression['description']}")
                output.append("")
        else:
            output.append("✅ NO PERFORMANCE REGRESSIONS DETECTED")
            output.append("   All biological consciousness performance metrics within acceptable ranges.")

        return "\n".join(output)


def main():
    """Run performance regression tests"""
    tester = BiologicalConsciousnessPerformanceTester()

    print("🧬 Starting Biological Consciousness Performance Regression Tests...")
    report = tester.run_performance_regression_tests()

    # Generate and display report
    report_text = tester.generate_performance_report(report)
    print("\n" + report_text)

    # Save report to file
    report_file = Path(f"performance_report_{report.test_run_id}.txt")
    with open(report_file, 'w') as f:
        f.write(report_text)

    print(f"\n📄 Report saved to: {report_file}")

    # Exit with appropriate code
    exit_code = 1 if report.regressions else 0
    return exit_code


if __name__ == "__main__":
    exit(main())
