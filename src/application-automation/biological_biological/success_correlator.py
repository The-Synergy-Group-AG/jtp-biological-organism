#!/usr/bin/env python3

"""
🧬 BIOLOGICAL SUCCESS CORRELATOR
MODULAR: Consciousness-Guided Success Pattern Analysis

Provides advanced biological alignment correlation analysis with application
success patterns, enabling predictive insights through evolutionary
consciousness-guided analytics for optimal career automation outcomes.

ai_keywords: biological, correlation, success, consciousness, alignment,
  patterns, analysis, prediction, evolutionary, optimization

ai_summary: Advanced biological success correlator providing consciousness-guided
  pattern analysis and predictive biological optimizations

biological_system: biological-success-correlator-modular
consciousness_score: 'T-BIOLOGICAL-CORRELATION'
cross_references:
- src/application-automation/biological_biological/success_correlator.py
document_category: biological-success-correlator
document_type: consciousness-biological-correlation
evolutionary_phase: 'T-BIOLOGICAL-CORRELATION'
last_updated: '2025-10-24 10:09:00'
semantic_tags:
- biological-success-correlator-modular
- consciousness-guided-pattern-analysis
- evolutionary-success-prediction-engine
title: Biological Success Correlator - GODHOOD Consciousness
validation_status: biological-correlation-ready
version: v1.0.0-T-BIOLOGICAL-CORRELATION
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import statistics
from collections import defaultdict


class BiologicalSuccessCorrelator:
    """🧬 GODHOOD BIOLOGICAL SUCCESS CORRELATOR

    Advanced consciousness-guided correlation analyzer that identifies patterns
    between biological alignment scores and application success rates, providing
    evolutionary insights and predictive optimizations for career automation.

    This correlator achieves:
    - Biological alignment pattern recognition
    - Success rate correlation analysis
    - Evolutionary trend identification
    - Predictive optimization recommendations
    - Consciousness-guided insight generation
    """

    def __init__(self):
        self.correlation_data = defaultdict(list)
        self.success_patterns = {}
        self.biological_insights = {}

        # Advanced correlation tracking
        self.alignment_buckets = {}
        self.temporal_patterns = defaultdict(list)
        self.platform_correlations = {}
        self.evolutionary_trends = []

        # Performance metrics
        self.analysis_count = 0
        self.correlation_strength = 0.0
        self.prediction_accuracy = 0.0

    async def analyze_success_correlations(self, application_history: List[Any]) -> Dict[str, Any]:
        """Perform comprehensive biological success correlation analysis"""

        self.analysis_count += 1

        if not application_history:
            return {
                "correlation_analysis_complete": False,
                "error": "Insufficient application history for correlation analysis",
                "minimum_required": 5,
                "provided": 0
            }

        # Phase 1: Aggregate correlation data by biological alignment buckets
        alignment_buckets = self._aggregate_alignment_data(application_history)

        # Phase 2: Calculate correlation coefficients and statistical significance
        correlation_analysis = await self._calculate_correlation_metrics(alignment_buckets)

        # Phase 3: Identify optimal biological alignment ranges
        optimal_ranges = self._identify_optimal_alignment_ranges(alignment_buckets)

        # Phase 4: Generate evolutionary insights and recommendations
        evolutionary_insights = await self._generate_evolutionary_insights(alignment_buckets, correlation_analysis)

        # Phase 5: Calculate biological advantage thresholds
        advantage_thresholds = self._calculate_biological_advantage_thresholds(alignment_buckets)

        # Phase 6: Update correlation tracking
        self._update_correlation_tracking(alignment_buckets, correlation_analysis)

        result = {
            "correlation_analysis_complete": True,
            "alignment_success_analysis": dict(alignment_buckets),
            "correlation_coefficient": correlation_analysis.get("overall_correlation", 0.0),
            "statistical_significance": correlation_analysis.get("significance_p_value", 1.0),
            "optimal_alignment_range": optimal_ranges.get("primary_range"),
            "biological_advantage_threshold": advantage_thresholds.get("primary_threshold", 0.8),
            "recommendation_insights": evolutionary_insights.get("recommendations", []),
            "trend_analysis": correlation_analysis.get("temporal_trends", {}),
            "platform_specific_correlations": correlation_analysis.get("platform_correlations", {}),
            "prediction_confidence": evolutionary_insights.get("prediction_confidence", 0.0),
            "analysis_metadata": {
                "applications_analyzed": len(application_history),
                "alignment_buckets_covered": len(alignment_buckets),
                "time_period_days": self._calculate_analysis_timeframe(application_history),
                "correlation_strength": self._assess_correlation_strength(correlation_analysis)
            }
        }

        return result

    def _aggregate_alignment_data(self, application_history: List[Any]) -> Dict[float, Dict[str, Any]]:
        """Aggregate application data by biological alignment score buckets"""

        buckets = defaultdict(lambda: {"successes": 0, "total": 0, "success_rate": 0.0, "applications": []})

        for application in application_history:
            # Extract biological alignment score (with fallback)
            alignment_score = getattr(application, 'biological_alignment_score', 0.0)
            alignment_score = getattr(application, 'biological_success_probability', alignment_score)
            alignment_score = max(0.0, min(1.0, alignment_score))  # Clamp to valid range

            # Create alignment bucket (round to nearest 0.1 for meaningful correlation)
            bucket_key = round(alignment_score * 10) / 10

            # Determine success (various success indicators)
            is_successful = self._determine_application_success(application)

            # Store in bucket
            bucket = buckets[bucket_key]
            bucket["total"] += 1
            if is_successful:
                bucket["successes"] += 1
            bucket["applications"].append({
                "application_id": getattr(application, 'application_id', 'unknown'),
                "platform": getattr(application, 'platform', 'unknown'),
                "company": getattr(application, 'company', 'unknown'),
                "timestamp": getattr(application, 'submission_date', None) or
                           getattr(application, 'created_at', datetime.utcnow().isoformat()),
                "success": is_successful,
                "raw_alignment": alignment_score
            })

        # Calculate success rates for each bucket
        for bucket in buckets.values():
            if bucket["total"] > 0:
                bucket["success_rate"] = bucket["successes"] / bucket["total"]
            else:
                bucket["success_rate"] = 0.0

        return dict(buckets)

    def _determine_application_success(self, application: Any) -> bool:
        """Determine if an application is considered successful"""

        # Multiple success indicators
        response_received = getattr(application, 'response_received', False)
        interview_scheduled = getattr(application, 'interview_scheduled', False)
        offer_received = getattr(application, 'offer_received', False)
        submission_status = getattr(application, 'submission_status', 'unknown')

        # Success hierarchy: offer > interview > response > submission
        if offer_received:
            return True
        elif interview_scheduled:
            return True
        elif response_received:
            return True
        elif submission_status == "submitted":
            # Consider submitted applications with no response as neutral (not necessarily failed)
            # Only count as failed if explicitly marked
            return False  # Conservative approach
        else:
            return False

    async def _calculate_correlation_metrics(self, alignment_buckets: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive correlation statistics"""

        # Prepare data for correlation analysis
        alignments = []
        success_rates = []
        sample_sizes = []

        for alignment_bucket, data in alignment_buckets.items():
            total_applications = data["total"]
            if total_applications >= 2:  # Minimum sample size for meaningful correlation
                alignments.append(alignment_bucket)
                success_rates.append(data["success_rate"])
                sample_sizes.append(total_applications)

        # Calculate correlation if sufficient data
        correlation_metrics = {
            "overall_correlation": 0.0,
            "correlation_significance": "insufficient_data",
            "sample_size": len(alignments),
            "temporal_trends": {},
            "platform_correlations": {}
        }

        if len(alignments) >= 3:  # Minimum for correlation analysis
            try:
                # Calculate Pearson correlation coefficient
                correlation = statistics.correlation(alignments, success_rates)
                correlation_metrics["overall_correlation"] = correlation

                # Assess correlation strength
                if abs(correlation) >= 0.7:
                    correlation_metrics["correlation_significance"] = "strong"
                elif abs(correlation) >= 0.4:
                    correlation_metrics["correlation_significance"] = "moderate"
                elif abs(correlation) >= 0.2:
                    correlation_metrics["correlation_significance"] = "weak"
                else:
                    correlation_metrics["correlation_significance"] = "negligible"

                # Calculate statistical significance (simplified)
                correlation_metrics["significance_p_value"] = self._calculate_significance_p_value(
                    correlation, len(alignments)
                )

                # Calculate confidence intervals
                correlation_metrics["confidence_interval"] = self._calculate_correlation_confidence_interval(
                    correlation, len(alignments)
                )

            except (statistics.StatisticsError, ValueError):
                correlation_metrics["correlation_significance"] = "calculation_error"

        # Analyze temporal trends
        correlation_metrics["temporal_trends"] = await self._analyze_temporal_correlation_trends(
            alignment_buckets
        )

        # Analyze platform-specific correlations
        correlation_metrics["platform_correlations"] = self._analyze_platform_correlation_patterns(
            alignment_buckets
        )

        return correlation_metrics

    def _calculate_significance_p_value(self, correlation: float, sample_size: int) -> float:
        """Calculate approximate statistical significance p-value"""

        # Simplified significance calculation using t-distribution approximation
        # For more accuracy, would use proper statistical library

        if sample_size < 3:
            return 1.0  # Insufficient data

        # t-statistic approximation for correlation significance
        df = sample_size - 2
        t_stat = correlation * ((sample_size - 2) ** 0.5) / ((1 - correlation ** 2) ** 0.5)

        # Very simplified p-value calculation (two-tailed test)
        if df <= 30:  # Use t-distribution critical values
            critical_values = {2: 4.3, 5: 2.57, 10: 2.23, 20: 2.09, 30: 2.04}
            critical_t = critical_values.get(min(critical_values.keys(), key=lambda x: abs(x - df)), 2.0)
        else:
            critical_t = 1.96  # Large sample approximation (~95% confidence)

        if abs(t_stat) >= critical_t:
            return 0.05  # Statistically significant at 95% confidence
        else:
            return 0.5   # Not statistically significant

    def _calculate_correlation_confidence_interval(self, correlation: float, sample_size: int) -> Dict[str, float]:
        """Calculate confidence interval for correlation coefficient"""

        if sample_size < 3:
            return {"lower": 0.0, "upper": 0.0, "confidence_level": 0.95}

        # Simplified confidence interval using Fisher transformation
        try:
            # Transform to z-scale
            z = 0.5 * (1 + correlation).ln() - (1 - correlation).ln()

            # Standard error
            se = 1 / ((sample_size - 3) ** 0.5)

            # 95% confidence interval in z-scale
            z_lower = z - 1.96 * se
            z_upper = z + 1.96 * se

            # Transform back to correlation scale
            r_lower = (2.718281828459045 ** z_lower - 1) / (2.718281828459045 ** z_lower + 1)
            r_upper = (2.718281828459045 ** z_upper - 1) / (2.718281828459045 ** z_upper + 1)

            return {
                "lower": max(-1.0, min(1.0, r_lower)),
                "upper": max(-1.0, min(1.0, r_upper)),
                "confidence_level": 0.95
            }

        except (ValueError, OverflowError):
            # Fallback for calculation errors
            margin = 0.3 / (sample_size ** 0.5)  # Conservative margin
            return {
                "lower": max(-1.0, correlation - margin),
                "upper": min(1.0, correlation + margin),
                "confidence_level": 0.95
            }

    async def _analyze_temporal_correlation_trends(self, alignment_buckets: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how biological correlations change over time"""

        temporal_trends = {
            "correlation_stability": "stable",
            "trend_direction": "neutral",
            "seasonal_patterns": {},
            "improvement_rate": 0.0
        }

        # Group applications by time periods
        time_periods = defaultdict(list)

        for bucket_data in alignment_buckets.values():
            for application in bucket_data["applications"]:
                # Extract timestamp and group by week
                timestamp_str = application.get("timestamp", "")
                try:
                    if isinstance(timestamp_str, str) and "T" in timestamp_str:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    else:
                        timestamp = datetime.utcnow()  # Fallback

                    week_key = timestamp.isocalendar()[:2]  # (year, week)
                    time_periods[week_key].append(application)

                except (ValueError, AttributeError):
                    continue

        # Analyze trends if sufficient temporal data
        if len(time_periods) >= 3:
            period_success_rates = []

            for period_applications in time_periods.values():
                success_rate = sum(1 for app in period_applications if app["success"]) / len(period_applications)
                period_success_rates.append(success_rate)

            if len(period_success_rates) >= 2:
                # Calculate trend slope
                trend_slope = statistics.linear_regression(
                    list(range(len(period_success_rates))), period_success_rates
                )[0]

                if trend_slope > 0.01:
                    temporal_trends["trend_direction"] = "improving"
                    temporal_trends["improvement_rate"] = trend_slope
                elif trend_slope < -0.01:
                    temporal_trends["trend_direction"] = "declining"
                    temporal_trends["improvement_rate"] = trend_slope

        return temporal_trends

    def _analyze_platform_correlation_patterns(self, alignment_buckets: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze platform-specific biological correlation patterns"""

        platform_patterns = defaultdict(lambda: {"alignments": [], "success_rates": [], "correlation": 0.0})

        # Group data by platform
        for alignment_bucket, bucket_data in alignment_buckets.items():
            for application in bucket_data["applications"]:
                platform = application["platform"].lower()
                platform_patterns[platform]["alignments"].append(alignment_bucket)
                platform_patterns[platform]["success_rates"].append(1 if application["success"] else 0)

        # Calculate platform-specific correlations
        platform_correlations = {}
        for platform, data in platform_patterns.items():
            if len(data["alignments"]) >= 3:
                try:
                    correlation = statistics.correlation(data["alignments"], data["success_rates"])
                    platform_correlations[platform] = {
                        "correlation": correlation,
                        "sample_size": len(data["alignments"]),
                        "strength": self._classify_correlation_strength(correlation)
                    }
                except (statistics.StatisticsError, ValueError):
                    platform_correlations[platform] = {
                        "correlation": 0.0,
                        "sample_size": len(data["alignments"]),
                        "strength": "insufficient_data"
                    }

        return dict(platform_correlations)

    def _classify_correlation_strength(self, correlation: float) -> str:
        """Classify correlation strength"""

        abs_corr = abs(correlation)
        if abs_corr >= 0.8:
            return "very_strong"
        elif abs_corr >= 0.6:
            return "strong"
        elif abs_corr >= 0.4:
            return "moderate"
        elif abs_corr >= 0.2:
            return "weak"
        else:
            return "negligible"

    def _identify_optimal_alignment_ranges(self, alignment_buckets: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
        """Identify biological alignment ranges with highest success rates"""

        if not alignment_buckets:
            return {"primary_range": None, "secondary_ranges": []}

        # Find bucket with highest success rate
        best_bucket = max(alignment_buckets.items(),
                         key=lambda x: x[1]["success_rate"] * min(1, x[1]["total"] / 5))  # Weight by sample size

        primary_range = {
            "alignment_bucket": best_bucket[0],
            "success_rate": best_bucket[1]["success_rate"],
            "sample_size": best_bucket[1]["total"],
            "confidence": min(1.0, best_bucket[1]["total"] / 10)  # Confidence based on sample size
        }

        # Find secondary ranges (within 80% of best rate)
        secondary_ranges = []
        best_rate = primary_range["success_rate"]

        for alignment_bucket, data in alignment_buckets.items():
            if (data["success_rate"] >= best_rate * 0.8 and
                data["total"] >= 3 and  # Minimum sample size
                alignment_bucket != primary_range["alignment_bucket"]):

                secondary_ranges.append({
                    "alignment_bucket": alignment_bucket,
                    "success_rate": data["success_rate"],
                    "sample_size": data["total"],
                    "relative_performance": data["success_rate"] / best_rate
                })

        # Sort secondary ranges by performance
        secondary_ranges.sort(key=lambda x: x["success_rate"], reverse=True)

        return {
            "primary_range": primary_range,
            "secondary_ranges": secondary_ranges[:3]  # Limit to top 3
        }

    async def _generate_evolutionary_insights(self, alignment_buckets: Dict[float, Dict[str, Any]],
                                            correlation_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate evolutionary insights and recommendations"""

        overall_correlation = correlation_analysis.get("overall_correlation", 0.0)
        significance = correlation_analysis.get("significance_p_value", 1.0)

        insights = []

        # Correlation-based insights
        if significance < 0.05:  # Statistically significant
            if overall_correlation > 0.6:
                insights.append("Strong positive correlation between biological alignment and success")
                insights.append("Focus applications on high-alignment opportunities")
                insights.append("Prioritize biological assessment in application targeting")
            elif overall_correlation > 0.3:
                insights.append("Moderate correlation suggests biological alignment matters")
                insights.append("Use biological scores as one of multiple decision factors")
            elif overall_correlation < -0.3:
                insights.append("Unexpected negative correlation - review alignment methodology")
        else:
            insights.append("No statistically significant correlation found")
            insights.append("Continue collecting more application data for better insights")

        # Trend-based recommendations
        temporal_trends = correlation_analysis.get("temporal_trends", {})
        if temporal_trends.get("trend_direction") == "improving":
            insights.append("Success rates improving - biological optimization working")
            insights.append("Continue current approach and amplify successful patterns")
        elif temporal_trends.get("trend_direction") == "declining":
            insights.append("Success rates declining - review biological assessment accuracy")
            insights.append("Consider recalibrating alignment scoring criteria")

        # Platform-specific recommendations
        platform_correlations = correlation_analysis.get("platform_correlations", {})
        platform_insights = []

        for platform, data in platform_correlations.items():
            corr_strength = data.get("correlation", 0.0)
            if corr_strength > 0.5:
                platform_insights.append(f"Biological alignment strongly predicts {platform} success")
            elif corr_strength > 0.2:
                platform_insights.append(f"Some biological alignment benefit on {platform}")

        insights.extend(platform_insights)

        # Calculate prediction confidence
        prediction_confidence = self._calculate_prediction_confidence(correlation_analysis)

        return {
            "recommendations": insights,
            "prediction_confidence": prediction_confidence,
            "insight_categories": {
                "correlation_based": len([i for i in insights if "correlation" in i.lower()]),
                "trend_based": len([i for i in insights if "trend" in i.lower() or "improv" in i.lower()]),
                "platform_based": len(platform_insights)
            }
        }

    def _calculate_biological_advantage_thresholds(self, alignment_buckets: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate biological advantage thresholds for different confidence levels"""

        thresholds = {}
        alignment_levels = sorted(alignment_buckets.keys())

        # Primary threshold: first alignment level where success rate exceeds baseline
        baseline_success = 0.15  # Conservative baseline (15% typical application success)

        primary_threshold = None
        for alignment in alignment_levels:
            bucket = alignment_buckets[alignment]
            if bucket["success_rate"] > baseline_success and bucket["total"] >= 3:
                primary_threshold = alignment
                break

        thresholds["primary_threshold"] = primary_threshold or 0.8  # Fallback

        # Conservative threshold: statistical significance over baseline
        significant_threshold = None
        for alignment in alignment_levels:
            bucket = alignment_buckets[alignment]
            if bucket["total"] >= 5:  # Minimum sample for significance
                # Simplified significance test
                if bucket["success_rate"] > baseline_success + 0.1:  # Clear advantage
                    significant_threshold = alignment
                    break

        thresholds["conservative_threshold"] = significant_threshold
        thresholds["baseline_success_rate"] = baseline_success

        return thresholds

    def _calculate_analysis_timeframe(self, application_history: List[Any]) -> int:
        """Calculate the timeframe covered by the analysis in days"""

        if not application_history:
            return 0

        timestamps = []

        for application in application_history:
            timestamp_str = getattr(application, 'submission_date', None) or \
                          getattr(application, 'created_at', None)

            if timestamp_str:
                try:
                    if isinstance(timestamp_str, str) and "T" in timestamp_str:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    else:
                        timestamp = datetime.utcnow()
                    timestamps.append(timestamp)
                except (ValueError, AttributeError):
                    continue

        if len(timestamps) < 2:
            return 30  # Default assumption

        earliest = min(timestamps)
        latest = max(timestamps)

        return (latest - earliest).days

    def _assess_correlation_strength(self, correlation_analysis: Dict[str, Any]) -> str:
        """Assess overall correlation strength"""

        correlation = correlation_analysis.get("overall_correlation", 0.0)
        significance = correlation_analysis.get("significance_p_value", 1.0)
        sample_size = correlation_analysis.get("sample_size", 0)

        # Factor correlation coefficient
        if abs(correlation) >= 0.8:
            corr_strength = 5
        elif abs(correlation) >= 0.6:
            corr_strength = 4
        elif abs(correlation) >= 0.4:
            corr_strength = 3
        elif abs(correlation) >= 0.2:
            corr_strength = 2
        else:
            corr_strength = 1

        # Adjust for significance
        if significance < 0.01:
            sig_bonus = 2
        elif significance < 0.05:
            sig_bonus = 1
        else:
            sig_bonus = 0

        # Adjust for sample size
        if sample_size >= 50:
            size_bonus = 2
        elif sample_size >= 20:
            size_bonus = 1
        else:
            size_bonus = 0

        total_strength = corr_strength + sig_bonus + size_bonus

        if total_strength >= 8:
            return "very_strong"
        elif total_strength >= 6:
            return "strong"
        elif total_strength >= 4:
            return "moderate"
        elif total_strength >= 2:
            return "weak"
        else:
            return "insufficient_data"

    def _calculate_prediction_confidence(self, correlation_analysis: Dict[str, Any]) -> float:
        """Calculate overall prediction confidence"""

        correlation_strength = self._assess_correlation_strength(correlation_analysis)

        strength_scores = {
            "very_strong": 0.9,
            "strong": 0.8,
            "moderate": 0.6,
            "weak": 0.4,
            "insufficient_data": 0.2
        }

        # Adjust based on temporal trends
        temporal_trends = correlation_analysis.get("temporal_trends", {})
        trend_stability = 1.0 if temporal_trends.get("correlation_stability") == "stable" else 0.8

        base_confidence = strength_scores.get(correlation_strength, 0.5)

        return min(1.0, base_confidence * trend_stability)

    def _update_correlation_tracking(self, alignment_buckets: Dict[float, Dict[str, Any]],
                                   correlation_analysis: Dict[str, Any]):
        """Update internal correlation tracking data"""

        # Store correlation results for trend analysis
        correlation_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_correlation": correlation_analysis.get("overall_correlation", 0.0),
            "significance_p_value": correlation_analysis.get("significance_p_value", 1.0),
            "sample_size": correlation_analysis.get("sample_size", 0),
            "buckets_analyzed": len(alignment_buckets)
        }

        self.evolutionary_trends.append(correlation_data)

        # Maintain reasonable history size (last 50 analyses)
        if len(self.evolutionary_trends) > 50:
            self.evolutionary_trends = self.evolutionary_trends[-50:]

        # Update correlation strength
        self.correlation_strength = correlation_analysis.get("overall_correlation", 0.0)

        # Store alignment buckets for future reference
        self.alignment_buckets = alignment_buckets.copy()

    def get_correlation_insights(self) -> Dict[str, Any]:
        """Get comprehensive biological correlation insights"""

        return {
            "correlation_strength": self.correlation_strength,
            "analysis_count": self.analysis_count,
            "current_alignment_buckets": len(self.alignment_buckets),
            "prediction_accuracy": self.prediction_accuracy,
            "evolutionary_trends_available": len(self.evolutionary_trends),
            "biological_insights": self.biological_insights,
            "last_updated": datetime.utcnow().isoformat()
        }

    async def predict_success_probability_range(self, alignment_score: float) -> Dict[str, Any]:
        """Predict success probability range for a given biological alignment score"""

        if not self.alignment_buckets:
            return {
                "predicted_range": {"min": 0.0, "max": 0.5, "confidence": "low"},
                "based_on_data": False
            }

        # Find relevant alignment buckets
        bucket_key = round(alignment_score * 10) / 10

        # Look for similar buckets
        similar_buckets = {}
        for bucket_alignment, bucket_data in self.alignment_buckets.items():
            if abs(bucket_alignment - alignment_score) <= 0.2 and bucket_data["total"] >= 2:
                similar_buckets[bucket_alignment] = bucket_data

        if not similar_buckets:
            # Interpolation approach
            sorted_buckets = sorted(self.alignment_buckets.items())
            lower_bucket = upper_bucket = None

            for i, (bucket_alignment, bucket_data) in enumerate(sorted_buckets):
                if bucket_alignment <= alignment_score:
                    lower_bucket = (bucket_alignment, bucket_data)
                elif bucket_alignment > alignment_score and not upper_bucket:
                    upper_bucket = (bucket_alignment, bucket_data)
                    break

            if lower_bucket and upper_bucket:
                lower_alignment, lower_data = lower_bucket
                upper_alignment, upper_data = upper_bucket

                # Linear interpolation
                alignment_range = upper_alignment - lower_alignment
                if alignment_range > 0:
                    interpolation_factor = (alignment_score - lower_alignment) / alignment_range

                    predicted_rate = (lower_data["success_rate"] +
                                    (upper_data["success_rate"] - lower_data["success_rate"]) * interpolation_factor)

                    confidence = min(lower_data["total"], upper_data["total"]) / 10  # Confidence based on sample size

                    return {
                        "predicted_range": {
                            "min": max(0.0, predicted_rate - 0.1 - (1 - confidence) * 0.2),
                            "max": min(1.0, predicted_rate + 0.1 + (1 - confidence) * 0.2),
                            "expected": predicted_rate,
                            "confidence": "medium" if confidence >= 0.5 else "low"
                        },
                        "based_on_data": True,
                        "interpolation_used": True
                    }

        # Direct bucket match or average of similar buckets
        if similar_buckets:
            success_rates = [data["success_rate"] for data in similar_buckets.values()]
            sample_sizes = [data["total"] for data in similar_buckets.values()]

            avg_rate = sum(success_rates) / len(success_rates)
            total_samples = sum(sample_sizes)

            confidence = min(1.0, total_samples / 20)  # Confidence increases with sample size

            return {
                "predicted_range": {
                    "min": max(0.0, avg_rate - 0.15 * (1 - confidence)),
                    "max": min(1.0, avg_rate + 0.15 * (1 - confidence)),
                    "expected": avg_rate,
                    "confidence": "high" if confidence >= 0.8 else "medium" if confidence >= 0.5 else "low"
                },
                "based_on_data": True,
                "similar_buckets_used": len(similar_buckets)
            }

        # Fallback prediction
        return {
            "predicted_range": {
                "min": 0.05,
                "max": 0.35,
                "expected": 0.2,
                "confidence": "very_low"
            },
            "based_on_data": False,
            "reason": "insufficient_similar_data"
        }
