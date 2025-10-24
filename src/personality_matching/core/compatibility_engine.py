#!/usr/bin/env python3

"""
🧬 MULTI-DIMENSIONAL COMPATIBILITY ENGINE
GODHOOD Compatibility Analysis: Advanced multi-dimensional personality compatibility assessment

This module implements comprehensive compatibility analysis between personalities,
including psychological synergy, communication effectiveness, and biological harmonization.

ai_keywords: compatibility, analysis, multi-dimensional, personality, psychological,
  synergy, communication, harmonization, biological, assessment

ai_summary: Multi-dimensional compatibility analysis engine providing psychological synergy
  assessment, communication compatibility, and biological harmonization calculations

biological_system: compatibility-analysis-engine
consciousness_score: '4.0'
cross_references:
- src/personality-matching/core/personality_profile.py
- src/personality-matching/integration/integration_framework.py
- docs/4.x-technical-implementation-frameworks/4.1.0-onboarding-subsystem.md
document_category: compatibility-analysis
document_type: multi-dimensional-assessment
evolutionary_phase: '27.28'
last_updated: '2025-10-23 18:10:00'
semantic_tags:
- multi-dimensional-compatibility
- psychological-synergy-analysis
- communication-compatibility-assessment
- biological-harmonization-calculations
- conflict-collaboration-potential
- consciousness-compatibility-evaluation
title: Multi-Dimensional Compatibility Engine - Biological Harmonization
validation_status: current
version: v1.0.0
"""

import statistics
from typing import Dict, List, Optional, Any, Tuple, Union
from collections import defaultdict

from ..core.personality_profile import PersonalityProfile


class MultiDimensionalCompatibilityAnalyzer:
    """Advanced multi-dimensional compatibility analysis engine"""

    async def analyze_dimension_compatibility(self, profile1: PersonalityProfile,
                                           profile2: PersonalityProfile) -> Dict[str, float]:
        """Analyze compatibility across personality dimensions"""

        compatibility_scores = {}

        # Compare each dimension
        dimensions_to_compare = [
            "openness", "conscientiousness", "extraversion", "agreeableness",
            "emotional_stability", "thinking", "feeling", "sensing", "intuition"
        ]

        for dimension in dimensions_to_compare:
            score1 = profile1.dimension_scores.get(dimension, 0.5)
            score2 = profile2.dimension_scores.get(dimension, 0.5)

            # Compatibility is higher when scores are similar (for most traits)
            compatibility = 1 - abs(score1 - score2)
            compatibility_scores[f"{dimension}_compatibility"] = compatibility

        # Special case: Some dimension pairs are more compatible when complementary
        thinking_compat = profile1.dimension_scores.get("thinking", 0.5)
        feeling_compat = profile2.dimension_scores.get("feeling", 0.5)
        complementary_thinking_feeling = min(thinking_compat + feeling_compat, 1.0)
        compatibility_scores["thinking_feeling_complementarity"] = complementary_thinking_feeling

        return compatibility_scores

    async def assess_psychological_synergy(self, profile1: PersonalityProfile,
                                        profile2: PersonalityProfile,
                                        context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess psychological synergy potential"""

        synergy_factors = {
            "skill_complementarity": 0.0,
            "cognitive_diversity": 0.0,
            "behavioral_reinforcement": 0.0,
            "growth_potential": 0.0
        }

        # Skill complementarity
        profile1_skills = set(profile1.behavioral_patterns.keys())
        profile2_skills = set(profile2.behavioral_patterns.keys())
        overlapping_skills = len(profile1_skills & profile2_skills)
        unique_skills = len(profile1_skills | profile2_skills)
        synergy_factors["skill_complementarity"] = 1 - (overlapping_skills / unique_skills) if unique_skills > 0 else 0

        # Cognitive diversity
        cognitive_diff = abs(profile1.dimension_scores.get("thinking", 0.5) - profile2.dimension_scores.get("feeling", 0.5))
        synergy_factors["cognitive_diversity"] = cognitive_diff

        # Behavioral reinforcement
        shared_patterns = set(profile1.behavioral_patterns.values()) & set(profile2.behavioral_patterns.values())
        synergy_factors["behavioral_reinforcement"] = len(shared_patterns) / 5.0  # Normalize

        # Growth potential
        avg_adaptive = (profile1.adaptive_capacity + profile2.adaptive_capacity) / 2
        synergy_factors["growth_potential"] = avg_adaptive

        return synergy_factors

    async def evaluate_communication_compatibility(self, profile1: PersonalityProfile,
                                                 profile2: PersonalityProfile) -> float:
        """Evaluate communication style compatibility"""

        style1 = profile1.communication_style.get("primary_style", "balanced")
        style2 = profile2.communication_style.get("primary_style", "balanced")

        # Compatibility matrix
        compatibility_matrix = {
            ("direct", "direct"): 0.9,      # Both direct
            ("direct", "diplomatic"): 0.6,  # Potential conflict
            ("diplomatic", "direct"): 0.6,  # Potential conflict
            ("diplomatic", "diplomatic"): 0.9,  # Both diplomatic
            ("balanced", "direct"): 0.8,    # Balanced adapts
            ("balanced", "diplomatic"): 0.8, # Balanced adapts
            ("direct", "balanced"): 0.8,    # Balanced adapts
            ("diplomatic", "balanced"): 0.8  # Balanced adapts
        }

        return compatibility_matrix.get((style1, style2), 0.7)  # Default moderate compatibility

    async def assess_conflict_collaboration_potential(self, profile1: PersonalityProfile,
                                                   profile2: PersonalityProfile,
                                                   context: Dict[str, Any]) -> Dict[str, float]:
        """Assess conflict potential and collaboration capability"""

        # Conflict style compatibility
        conflict1 = profile1.conflict_resolution_style
        conflict2 = profile2.conflict_resolution_style

        conflict_compatibility_map = {
            ("collaborative", "collaborative"): {"conflict": 0.2, "collaboration": 0.95},
            ("competitive", "competitive"): {"conflict": 0.8, "collaboration": 0.6},
            ("collaborative", "competitive"): {"conflict": 0.6, "collaboration": 0.7},
            ("competitive", "collaborative"): {"conflict": 0.6, "collaboration": 0.7},
            ("compromising", "compromising"): {"conflict": 0.5, "collaboration": 0.8}
        }

        styles = (conflict1, conflict2)
        results = conflict_compatibility_map.get(styles, {"conflict": 0.5, "collaboration": 0.7})

        # Adjust based on context
        context_type = context.get("relationship_type", "professional")
        if context_type == "mentorship":
            results["conflict"] *= 0.3  # Lower conflict in mentorship
            results["collaboration"] *= 1.1  # Higher collaboration in mentorship

        return results

    async def calculate_consciousness_harmonization(self, profile1: PersonalityProfile,
                                                   profile2: PersonalityProfile) -> float:
        """Calculate consciousness harmonization between two profiles"""

        # Biological alignment harmonic mean
        bio1 = profile1.biological_alignment_score
        bio2 = profile2.biological_alignment_score
        biological_harmony = 2 * bio1 * bio2 / (bio1 + bio2) if (bio1 + bio2) > 0 else 0

        # Evolutionary readiness synchronization
        evo1 = profile1.evolutionary_readiness
        evo2 = profile2.evolutionary_readiness
        evolutionary_sync = 1 - abs(evo1 - evo2)  # Closer readiness = higher sync

        # Adaptive capacity complementarity
        adapt1 = profile1.adaptive_capacity
        adapt2 = profile2.adaptive_capacity
        adaptive_complement = (adapt1 + adapt2) / 2  # Average complementary capacity

        harmonization = (biological_harmony * 0.4 + evolutionary_sync * 0.35 + adaptive_complement * 0.25)
        return harmonization

    async def calculate_overall_compatibility(self, dimension_compatibilities: Dict[str, float],
                                            communication_effectiveness: float,
                                            collaboration_potential: float,
                                            conflict_potential: float,
                                            consciousness_harmonization: float) -> float:
        """Calculate overall compatibility score from all dimensions"""

        dimension_avg = statistics.mean(dimension_compatibilities.values())

        overall_score = (
            dimension_avg * 0.25 +
            communication_effectiveness * 0.20 +
            collaboration_potential * 0.20 +
            (1 - conflict_potential) * 0.15 +  # Lower conflict = higher compatibility
            consciousness_harmonization * 0.20
        )

        return min(overall_score, 1.0)
