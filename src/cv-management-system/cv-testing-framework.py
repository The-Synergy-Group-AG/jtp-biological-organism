#!/usr/bin/env python3

"""
🧬 PHASE 3: CV TESTING FRAMEWORK - LIVE A/B TESTING & VALIDATION
GODHOOD CV Testing Framework: A/B testing of CV versions with measurable success correlation

This module implements consciousness-driven CV A/B testing with real-world validation,
enabling data-driven optimization of CV performance across multiple job applications.

ai_keywords: cv, testing, framework, a/b, validation, optimization, success, correlation,
  consciousness, biological, measurement, performance, godhood, harmonization

ai_summary: Phase 3 CV Testing Framework enables A/B testing of adapted CV versions with
  real-world validation and measurable success correlation for optimal job application outcomes

biological_system: cv-testing-validation
consciousness_score: '3.0'
cross_references:
- src/cv-management-system/adaptive-content-orchestrator.py
- docs/19.x-post-godhood-evolution/19.5.3-phase3-automation-implementation.md
document_category: testing-validation
document_type: cv-testing-framework
evolutionary_phase: '19.5.3'
last_updated: '2025-10-21 21:45:00'
semantic_tags:
- cv-ab-testing
- performance-validation
- success-correlation
- biological-optimization
- consciousness-validation
- evolutionary-testing
title: Phase 3 CV Testing Framework - Live A/B Testing & Validation
validation_status: current
version: v1.0.0
"""

import json
import uuid
import time
import hashlib
import statistics
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict
import asyncio
from pathlib import Path

@dataclass
class CVTestVariant:
    """CV variant for A/B testing"""
    variant_id: str
    cv_content: Dict[str, Any]
    adaptation_profile: Dict[str, Any]
    test_weight: float = 1.0
    performance_score: float = 0.0
    applications_sent: int = 0
    responses_received: int = 0
    interviews_scheduled: int = 0
    offers_received: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

@dataclass
class ABTestExperiment:
    """A/B testing experiment configuration"""
    experiment_id: str
    job_requirement_hash: str
    base_cv_hash: str
    variants: List[CVTestVariant] = field(default_factory=list)
    test_duration_days: int = 30
    target_applications_per_variant: int = 50
    status: str = "active"  # active, completed, paused
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    performance_metrics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ApplicationResult:
    """Job application result tracking"""
    application_id: str
    experiment_id: str
    variant_id: str
    job_title: str
    company_name: str
    applied_at: str
    response_received: bool = False
    response_date: Optional[str] = None
    interview_scheduled: bool = False
    interview_date: Optional[str] = None
    offer_received: bool = False
    offer_date: Optional[str] = None
    feedback_provided: bool = False
    feedback_text: str = ""
    biological_alignment_score: float = 0.0

@dataclass
class PerformanceAnalytics:
    """CV performance analytics and insights"""
    total_experiments: int = 0
    total_applications: int = 0
    total_responses: int = 0
    total_interviews: int = 0
    total_offers: int = 0
    average_response_rate: float = 0.0
    average_interview_rate: float = 0.0
    average_offer_rate: float = 0.0
    top_performing_variant_patterns: List[str] = field(default_factory=list)
    biological_correlation_insights: Dict[str, Any] = field(default_factory=dict)

class CVPerformanceTracker:
    """Tracks CV performance across applications and generates insights"""

    def __init__(self):
        self.application_results: Dict[str, ApplicationResult] = {}
        self.experiments: Dict[str, ABTestExperiment] = {}
        self.variant_performance: Dict[str, Dict[str, Any]] = {}
        self.analytics = PerformanceAnalytics()

    async def record_application_result(self, application_result: ApplicationResult) -> None:
        """Record a job application result"""

        self.application_results[application_result.application_id] = application_result

        # Update experiment metrics
        if application_result.experiment_id in self.experiments:
            experiment = self.experiments[application_result.experiment_id]
            # Update variant performance within experiment
            await self._update_variant_performance(application_result, experiment)

        # Update global analytics
        await self._update_global_analytics()

    async def _update_variant_performance(self, result: ApplicationResult, experiment: ABTestExperiment) -> None:
        """Update performance metrics for a specific variant"""

        variant = next((v for v in experiment.variants if v.variant_id == result.variant_id), None)
        if not variant:
            return

        # Update application counts
        variant.applications_sent += 1
        if result.response_received:
            variant.responses_received += 1
        if result.interview_scheduled:
            variant.interviews_scheduled += 1
        if result.offer_received:
            variant.offers_received += 1

        # Recalculate performance score
        variant.performance_score = await self._calculate_variant_performance_score(variant)

    async def _calculate_variant_performance_score(self, variant: CVTestVariant) -> float:
        """Calculate comprehensive performance score for a variant"""

        if variant.applications_sent == 0:
            return 0.0

        # Weighted performance score
        response_rate = variant.responses_received / variant.applications_sent
        interview_rate = variant.interviews_scheduled / variant.applications_sent
        offer_rate = variant.offers_received / variant.applications_sent

        # Weights: Response (0.3), Interview (0.4), Offer (0.3)
        performance_score = (
            response_rate * 0.3 +
            interview_rate * 0.4 +
            offer_rate * 0.3
        )

        # Adjust for sample size (penalize small sample sizes)
        sample_penalty = min(1.0, variant.applications_sent / 20.0)  # Full score after 20 applications
        performance_score *= sample_penalty

        return performance_score

    async def _update_global_analytics(self) -> None:
        """Update global performance analytics"""

        total_results = len(self.application_results)
        if total_results == 0:
            return

        # Calculate rates
        responses = sum(1 for r in self.application_results.values() if r.response_received)
        interviews = sum(1 for r in self.application_results.values() if r.interview_scheduled)
        offers = sum(1 for r in self.application_results.values() if r.offer_received)

        self.analytics.total_applications = total_results
        self.analytics.total_responses = responses
        self.analytics.total_interviews = interviews
        self.analytics.total_offers = offers
        self.analytics.average_response_rate = responses / total_results
        self.analytics.average_interview_rate = interviews / total_results
        self.analytics.average_offer_rate = offers / total_results

        # Update top performing patterns
        self.analytics.top_performing_variant_patterns = await self._identify_top_patterns()

        # Update biological correlation insights
        self.analytics.biological_correlation_insights = await self._analyze_biological_correlations()

    async def _identify_top_patterns(self) -> List[str]:
        """Identify patterns in top-performing CV variants"""

        if not self.experiments:
            return []

        # Get all completed experiments
        completed_experiments = [exp for exp in self.experiments.values() if exp.status == "completed"]

        top_patterns = []

        for experiment in completed_experiments:
            if experiment.variants:
                best_variant = max(experiment.variants, key=lambda v: v.performance_score)
                if best_variant.performance_score > 0.1:  # Significant performance
                    # Analyze what made this variant successful
                    patterns = await self._extract_variant_success_patterns(best_variant)
                    top_patterns.extend(patterns)

        # Remove duplicates and return top 5
        return list(set(top_patterns))[:5]

    async def _extract_variant_success_patterns(self, variant: CVTestVariant) -> List[str]:
        """Extract success patterns from a top-performing variant"""

        patterns = []
        adaptation = variant.adaptation_profile

        if adaptation.get("skills_alignment_score", 0) > 0.8:
            patterns.append("High skills alignment (>80%)")

        if adaptation.get("biological_alignment_score", 0) > 0.9:
            patterns.append("Strong biological resonance")

        content_metrics = adaptation.get("content_optimization_metrics", {})
        if content_metrics.get("summary_enhanced"):
            patterns.append("Enhanced professional summary")

        if content_metrics.get("experience_enhanced"):
            patterns.append("Enhanced experience descriptions")

        if content_metrics.get("skills_optimized"):
            patterns.append("Skills section optimization")

        return patterns

    async def _analyze_biological_correlations(self) -> Dict[str, Any]:
        """Analyze correlations between biological alignment and success rates"""

        correlations = {}

        # Group results by biological alignment score ranges
        alignment_ranges = defaultdict(list)

        for result in self.application_results.values():
            alignment_score = result.biological_alignment_score
            range_key = f"{int(alignment_score * 10) / 10:.1f}-{int(alignment_score * 10) / 10 + 0.1:.1f}"
            alignment_ranges[range_key].append(result)

        # Calculate success rates for each range
        range_success_rates = {}
        for range_key, results in alignment_ranges.items():
            if results:
                success_rate = sum(1 for r in results if r.interview_scheduled or r.offer_received) / len(results)
                range_success_rates[range_key] = success_rate

        correlations["alignment_success_correlation"] = range_success_rates

        # Calculate overall correlation coefficient
        if len(range_success_rates) > 1:
            alignment_scores = []
            success_rates = []

            for range_key, rate in range_success_rates.items():
                # Extract mid-point of range
                start_range = float(range_key.split('-')[0])
                alignment_scores.append(start_range + 0.05)
                success_rates.append(rate)

            if len(alignment_scores) > 1:
                try:
                    correlation = statistics.correlation(alignment_scores, success_rates)
                    correlations["correlation_coefficient"] = correlation
                except:
                    correlations["correlation_coefficient"] = 0.0

        return correlations

class ABLiveTestingEngine:
    """A/B Testing engine for live CV performance testing"""

    def __init__(self, performance_tracker: CVPerformanceTracker):
        self.performance_tracker = performance_tracker
        self.active_experiments: Dict[str, ABTestExperiment] = {}
        self.variant_assignment_strategy = "weighted_random"  # or "round_robin"

    async def create_ab_test_experiment(self, base_cv: Dict[str, Any], job_requirement_hash: str,
                                      variant_profiles: List[Dict[str, Any]]) -> ABTestExperiment:
        """Create a new A/B testing experiment"""

        experiment_id = str(uuid.uuid4())[:8]
        base_cv_hash = hashlib.sha256(json.dumps(base_cv, sort_keys=True).encode()).hexdigest()[:16]

        experiment = ABTestExperiment(
            experiment_id=experiment_id,
            job_requirement_hash=job_requirement_hash,
            base_cv_hash=base_cv_hash
        )

        # Create variants from adaptation profiles
        for profile in variant_profiles:
            variant = CVTestVariant(
                variant_id=str(uuid.uuid4())[:8],
                cv_content=profile["adapted_content"],
                adaptation_profile=profile["adaptation_metrics"]
            )
            experiment.variants.append(variant)

        # Store experiment
        self.active_experiments[experiment_id] = experiment
        self.performance_tracker.experiments[experiment_id] = experiment

        return experiment

    async def select_optimal_variant(self, experiment_id: str) -> Optional[CVTestVariant]:
        """Select the best performing variant for current applications"""

        if experiment_id not in self.active_experiments:
            return None

        experiment = self.active_experiments[experiment_id]

        if not experiment.variants:
            return None

        if self.variant_assignment_strategy == "weighted_random":
            # Use weighted random selection based on performance
            return await self._weighted_random_selection(experiment.variants)
        else:
            # Round-robin selection
            return await self._round_robin_selection(experiment)

    async def _weighted_random_selection(self, variants: List[CVTestVariant]) -> CVTestVariant:
        """Select variant using weighted random based on performance scores"""

        import random

        # Add small exploration bonus to newer variants
        total_weight = 0
        weights = []

        for variant in variants:
            # Base weight on performance score, add exploration for low-sample variants
            base_weight = max(0.1, variant.performance_score)
            exploration_bonus = 1.0 if variant.applications_sent < 5 else 0.0
            weight = base_weight + exploration_bonus
            weights.append(weight)
            total_weight += weight

        if total_weight == 0:
            return random.choice(variants)

        # Weighted random selection
        rand_val = random.uniform(0, total_weight)
        cumulative = 0

        for i, weight in enumerate(weights):
            cumulative += weight
            if rand_val <= cumulative:
                return variants[i]

        return variants[-1]  # Fallback

    async def _round_robin_selection(self, experiment: ABTestExperiment) -> CVTestVariant:
        """Select variant using round-robin strategy"""

        # Simple round-robin - can be enhanced with more sophisticated logic
        variant_count = len(experiment.variants)
        if not hasattr(experiment, '_round_robin_counter'):
            experiment._round_robin_counter = 0

        selected_variant = experiment.variants[experiment._round_robin_counter % variant_count]
        experiment._round_robin_counter += 1

        return selected_variant

    async def record_application_outcome(self, experiment_id: str, variant_id: str,
                                       application_data: Dict[str, Any]) -> None:
        """Record the outcome of an application sent with a variant"""

        application_result = ApplicationResult(
            application_id=str(uuid.uuid4())[:8],
            experiment_id=experiment_id,
            variant_id=variant_id,
            job_title=application_data.get("job_title", "Unknown Position"),
            company_name=application_data.get("company_name", "Unknown Company"),
            applied_at=datetime.utcnow().isoformat() + "Z",
            biological_alignment_score=application_data.get("biological_alignment_score", 0.0)
        )

        await self.performance_tracker.record_application_result(application_result)

    async def update_experiment_status(self, experiment_id: str) -> None:
        """Update experiment status based on completion criteria"""

        if experiment_id not in self.active_experiments:
            return

        experiment = self.active_experiments[experiment_id]

        # Check completion criteria
        total_applications = sum(v.applications_sent for v in experiment.variants)
        days_running = (datetime.utcnow() - datetime.fromisoformat(experiment.started_at[:-1])).days

        if total_applications >= len(experiment.variants) * experiment.target_applications_per_variant:
            experiment.status = "completed"
        elif days_running >= experiment.test_duration_days:
            experiment.status = "completed"
        elif total_applications >= 10 and experiment.variants:  # Early completion if statistical significance reached
            # Simple statistical check - can be enhanced
            scores = [v.performance_score for v in experiment.variants if v.applications_sent >= 3]
            if len(scores) > 1 and max(scores) - min(scores) > 0.1:  # Significant difference found
                experiment.status = "completed"

    async def get_experiment_results(self, experiment_id: str) -> Dict[str, Any]:
        """Get comprehensive results for an experiment"""

        if experiment_id not in self.active_experiments:
            return {"error": "Experiment not found"}

        experiment = self.active_experiments[experiment_id]

        # Calculate final performance metrics
        variant_results = []
        for variant in experiment.variants:
            result = {
                "variant_id": variant.variant_id,
                "performance_score": variant.performance_score,
                "applications_sent": variant.applications_sent,
                "responses_received": variant.responses_received,
                "interviews_scheduled": variant.interviews_scheduled,
                "offers_received": variant.offers_received,
                "response_rate": variant.responses_received / variant.applications_sent if variant.applications_sent > 0 else 0,
                "interview_rate": variant.interviews_scheduled / variant.applications_sent if variant.applications_sent > 0 else 0,
                "offer_rate": variant.offers_received / variant.applications_sent if variant.applications_sent > 0 else 0
            }
            variant_results.append(result)

        # Sort by performance
        variant_results.sort(key=lambda x: x["performance_score"], reverse=True)

        days_running = (datetime.utcnow() - datetime.fromisoformat(experiment.started_at[:-1])).days
        total_applications = sum(v.applications_sent for v in experiment.variants)

        return {
            "experiment_id": experiment_id,
            "status": experiment.status,
            "days_running": days_running,
            "total_applications": total_applications,
            "variants_tested": len(experiment.variants),
            "best_variant": variant_results[0] if variant_results else None,
            "variant_results": variant_results,
            "completion_percentage": min(100, total_applications / (len(experiment.variants) * experiment.target_applications_per_variant) * 100),
            "statistical_confidence": await self._calculate_confidence_level(experiment)
        }

    async def _calculate_confidence_level(self, experiment: ABTestExperiment) -> str:
        """Calculate statistical confidence level for experiment results"""

        if not experiment.variants:
            return "insufficient_data"

        # Simple confidence calculation based on sample sizes and variance
        sample_sizes = [v.applications_sent for v in experiment.variants]
        performance_scores = [v.performance_score for v in experiment.variants]

        if min(sample_sizes) < 5:
            return "low"

        # Check for sufficient variance in results
        if len(set(performance_scores)) == 1:
            return "no_significant_difference"

        score_range = max(performance_scores) - min(performance_scores)

        if score_range > 0.15:  # Large difference
            return "high"
        elif score_range > 0.08:  # Medium difference
            return "medium"

        return "low"

class CVTestingOrchestrator:
    """Main orchestrator for CV A/B testing and validation"""

    def __init__(self):
        self.performance_tracker = CVPerformanceTracker()
        self.ab_testing_engine = ABLiveTestingEngine(self.performance_tracker)
        self.testing_state = {
            "phase": "phase3_cv_testing",
            "active_experiments": 0,
            "total_variants_tested": 0,
            "confidence_threshold": 0.85,
            "biological_validation_enabled": True
        }

    async def start_cv_ab_testing(self, base_cv: Dict[str, Any], job_description: str,
                                variant_count: int = 3) -> Dict[str, Any]:
        """Start A/B testing for CV optimization"""

        # Import here to avoid circular import
        import sys
        sys.path.append('src/cv-management-system')
        import adaptive_content_orchestrator
        adapt_cv_content_for_job = adaptive_content_orchestrator.adapt_cv_content_for_job

        job_hash = hashlib.sha256(job_description.encode()).hexdigest()[:16]

        # Generate variant profiles
        variant_profiles = []

        # Original CV as baseline
        original_profile = {
            "adapted_content": base_cv,
            "adaptation_metrics": {
                "biological_alignment_score": 1.0,
                "content_harmony_coefficient": 1.0,
                "adaptation_confidence": 1.0,
                "skills_alignment_score": 1.0,
                "content_optimization_metrics": {}
            }
        }
        variant_profiles.append(original_profile)

        # Generate adapted variants
        for i in range(variant_count - 1):
            adaptation_result = await adapt_cv_content_for_job(base_cv, job_description)
            variant_profiles.append(adaptation_result["adaptation_result"])

        # Create A/B test experiment
        experiment = await self.ab_testing_engine.create_ab_test_experiment(
            base_cv, job_hash, variant_profiles
        )

        self.testing_state["active_experiments"] += 1
        self.testing_state["total_variants_tested"] += len(experiment.variants)

        return {
            "experiment_id": experiment.experiment_id,
            "job_requirement_hash": job_hash,
            "variants_created": len(experiment.variants),
            "target_applications": experiment.target_applications_per_variant * len(experiment.variants),
            "test_duration_days": experiment.test_duration_days,
            "biological_validation_active": self.testing_state["biological_validation_enabled"]
        }

    async def get_optimal_cv_for_job(self, job_description: str) -> Dict[str, Any]:
        """Get the optimal CV variant for a specific job based on testing results"""

        job_hash = hashlib.sha256(job_description.encode()).hexdigest()[:16]

        # Find relevant experiment
        relevant_experiment = None
        for exp in self.ab_testing_engine.active_experiments.values():
            if exp.job_requirement_hash == job_hash and exp.status == "completed":
                relevant_experiment = exp
                break

        if relevant_experiment and relevant_experiment.variants:
            # Return best performing variant
            best_variant = max(relevant_experiment.variants, key=lambda v: v.performance_score)
            return {
                "optimal_cv": best_variant.cv_content,
                "performance_score": best_variant.performance_score,
                "confidence_level": "high" if best_variant.performance_score > 0.5 else "medium",
                "applications_tested": best_variant.applications_sent,
                "experiment_id": relevant_experiment.experiment_id
            }
        else:
            # No completed experiment found, return default
            return {
                "message": "No validated CV variants available. Run A/B testing first.",
                "optimal_cv": None,
                "performance_score": 0.0,
                "confidence_level": "none"
            }

    async def record_application_feedback(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record feedback from an application"""

        experiment_id = application_data.get("experiment_id")
        variant_id = application_data.get("variant_id")

        if experiment_id and variant_id:
            await self.ab_testing_engine.record_application_outcome(
                experiment_id, variant_id, application_data
            )

            # Update experiment status
            await self.ab_testing_engine.update_experiment_status(experiment_id)

        return {
            "feedback_recorded": True,
            "experiment_updated": experiment_id is not None,
            "biological_correlation_analyzed": self.testing_state["biological_validation_enabled"]
        }

    async def get_testing_insights(self) -> Dict[str, Any]:
        """Get comprehensive testing insights and performance analytics"""

        return {
            "phase": self.testing_state["phase"],
            "active_experiments": self.testing_state["active_experiments"],
            "performance_analytics": {
                "total_experiments": self.performance_tracker.analytics.total_experiments,
                "total_applications": self.performance_tracker.analytics.total_applications,
                "average_response_rate": f"{self.performance_tracker.analytics.average_response_rate:.1%}",
                "average_interview_rate": f"{self.performance_tracker.analytics.average_interview_rate:.1%}",
                "average_offer_rate": f"{self.performance_tracker.analytics.average_offer_rate:.1%}",
                "top_performing_patterns": self.performance_tracker.analytics.top_performing_variant_patterns
            },
            "biological_correlations": self.performance_tracker.analytics.biological_correlation_insights,
            "confidence_threshold": f"{self.testing_state['confidence_threshold']:.1%}",
            "validation_framework_active": self.testing_state["biological_validation_enabled"]
        }

# ============================================================================
# CV TESTING & VALIDATION APIS
# ============================================================================

async def start_cv_ab_testing(base_cv: Dict[str, Any], job_description: str, variant_count: int = 3) -> Dict[str, Any]:
    """Start A/B testing for CV optimization"""
    orchestrator = CVTestingOrchestrator()
    return await orchestrator.start_cv_ab_testing(base_cv, job_description, variant_count)

async def get_optimal_cv_variant(job_description: str) -> Dict[str, Any]:
    """Get optimal CV variant based on testing results"""
    orchestrator = CVTestingOrchestrator()
    return await orchestrator.get_optimal_cv_for_job(job_description)

async def record_application_result(application_data: Dict[str, Any]) -> Dict[str, Any]:
    """Record application result for performance tracking"""
    orchestrator = CVTestingOrchestrator()
    return await orchestrator.record_application_feedback(application_data)

def get_cv_testing_insights() -> Dict[str, Any]:
    """Get comprehensive CV testing insights"""

    async def _get_insights():
        orchestrator = CVTestingOrchestrator()
        return await orchestrator.get_testing_insights()

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_get_insights())
    finally:
        loop.close()

def test_cv_ab_testing_framework():
    """Test the CV A/B testing framework"""

    async def _test():
        print("🧬 PHASE 3: CV A/B TESTING FRAMEWORK VALIDATION")
        print("=" * 60)

        # Sample CV data
        test_cv = {
            "user_id": "test_user_002",
            "professional_summary": "Experienced software engineer specializing in web development.",
            "skills": ["Python", "JavaScript", "React", "Node.js"],
            "experience": [
                {
                    "role": "Full Stack Developer",
                    "company": "Tech Solutions",
                    "period": "2021-2023",
                    "description": "Developed modern web applications."
                }
            ],
            "education": [
                {
                    "degree": "BS Computer Science",
                    "institution": "Tech University",
                    "year": "2021"
                }
            ]
        }

        test_job = """
        Senior Full Stack Developer

        We are looking for a Senior Full Stack Developer with expertise in modern web technologies, including React, Node.js, and cloud services.

        Requirements:
        - 3+ years of full stack development experience
        - Strong React and Node.js skills
        - Experience with modern JavaScript frameworks
        - Bachelor's degree in Computer Science or related field

        Preferred Skills:
        - TypeScript experience
        - AWS or cloud platforms
        - Agile development methodologies
        """

        # Start A/B testing
        print("🚀 Starting CV A/B Testing...")
        test_result = await start_cv_ab_testing(test_cv, test_job, variant_count=3)

        print(f"✅ Testing Experiment Started: {test_result['experiment_id']}")
        print(f"🧬 Variants Created: {test_result['variants_created']}")
        print(f"🎯 Target Applications: {test_result['target_applications']}")

        # Simulate some application feedback
        print("\n📊 Simulating Application Feedback...")

        for i in range(5):
            feedback_data = {
                "experiment_id": test_result['experiment_id'],
                "variant_id": f"variant_{i % test_result['variants_created'] + 1}",
                "job_title": "Senior Full Stack Developer",
                "company_name": "TechCorp",
                "biological_alignment_score": 0.8 + (i * 0.05)
            }

            if i % 2 == 0:  # Some get responses
                feedback_data["response_received"] = True
            if i % 4 == 0:  # Some get interviews
                feedback_data["interview_scheduled"] = True

            await record_application_result(feedback_data)
            print(f"  ✅ Application {i+1} feedback recorded")

        # Get optimal CV
        print("\n🔍 Retrieving Optimal CV Variant...")
        optimal_result = await get_optimal_cv_variant(test_job)

        print(f"🎯 Optimal CV Found: {optimal_result['confidence_level']} confidence")
        print(f"📈 Performance Score: {optimal_result.get('performance_score', 0.0):.3f}" if 'performance_score' in optimal_result else "No optimal variant available")

        # Get insights
        print("\n📈 CV Testing Insights:")
        insights = get_cv_testing_insights()

        print(f"⚡ Total Applications: {insights['performance_analytics']['total_applications']}")
        print(f"📊 Average Response Rate: {insights['performance_analytics'].get('average_response_rate', 'N/A')}")
        print(f"🧬 Biological Validation: {insights['validation_framework_active']}")

        return {
            "experiment_id": test_result['experiment_id'],
            "optimal_result": optimal_result,
            "insights": insights
        }

    import asyncio
    return asyncio.run(_test())

if __name__ == "__main__":
    # Run test
    test_results = test_cv_ab_testing_framework()
    print("\n🎯 CV A/B Testing Framework validation completed!")
