#!/usr/bin/env python3

"""
Multi-Dimensional Compatibility Engine - Personality Compatibility Analysis

Provides comprehensive compatibility analysis between personalities,
including psychological synergy and communication effectiveness.
"""

import statistics
from typing import Dict, List, Optional, Any, Tuple, Union
from collections import defaultdict

from ..core.personality_profile import PersonalityProfile
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CompatibilityAnalysis:
    """Analysis of compatibility between two personality profiles"""
    compatibility_id: str = ""
    primary_profile_id: str = ""
    secondary_profile_id: str = ""
    overall_compatibility: float = 0.0
    dimension_compatibilities: Dict[str, float] = field(default_factory=dict)
    psychological_synergy: Dict[str, Any] = field(default_factory=dict)
    communication_effectiveness: float = 0.0
    conflict_potential: float = 0.0
    collaboration_potential: float = 0.0
    consciousness_harmonization: float = 0.0
    biological_compatibility: float = 0.0
    recommendation_score: float = 0.0
    analysis_timestamp: Optional[str] = None


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

    # ============================================================================
    # TEST COMPATIBILITY METHODS: Real mathematical implementations
    # ============================================================================

    def calculate_multidimensional_compatibility(self, profile1_traits: Dict[str, float],
                                                    profile2_traits: Dict[str, float]) -> Dict[str, Any]:
        """Calculate multidimensional compatibility with real weighted algorithms"""

        # Calculate compatibility scores for each trait dimension
        compatibility_scores = {}
        weights = {
            "openness": 0.15,
            "conscientiousness": 0.25,
            "extraversion": 0.20,
            "agreeableness": 0.20,
            "emotional_stability": 0.20
        }

        for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "emotional_stability"]:
            score1 = profile1_traits.get(trait, 0.5)
            score2 = profile2_traits.get(trait, 0.5)
            # Compatibility decreases with trait difference (complementarity)
            compatibility = 1 - (abs(score1 - score2) * 0.8)  # 80% weight on difference
            compatibility_scores[trait] = max(0, min(1, compatibility))

        # Calculate weighted overall compatibility
        weighted_sum = sum(compatibility_scores.get(trait, 0.5) * weight
                          for trait, weight in weights.items())
        overall_compatibility = weighted_sum / sum(weights.values())

        # Add synergy bonus for complementary traits (e.g., high openness + high conscientiousness)
        synergy_bonus = 0
        if compatibility_scores.get("openness", 0) > 0.7 and compatibility_scores.get("conscientiousness", 0) > 0.7:
            synergy_bonus = 0.1  # Innovation + organization synergy

        final_compatibility = min(1.0, overall_compatibility + synergy_bonus)

        return {
            "overall_compatibility": final_compatibility,
            "dimensional_breakdown": compatibility_scores,
            "weighted_score": overall_compatibility,
            "synergy_bonus": synergy_bonus,
            "compatibility_factors": len(compatibility_scores)
        }

    def assess_values_compatibility(self, profile1_values: Dict[str, float],
                                       profile2_values: Dict[str, float]) -> Dict[str, Any]:
        """Assess values compatibility with real mathematical scoring"""

        # Core values that drive compatibility
        core_values = ["growth", "innovation", "stability", "relationships", "achievement"]
        compatibility_matrix = {}

        for value in core_values:
            val1 = profile1_values.get(value, 0.5)
            val2 = profile2_values.get(value, 0.5)

            # Values compatibility - higher when aligned
            alignment = 1 - abs(val1 - val2)
            compatibility_matrix[value] = alignment

        # Calculate core values alignment score
        if compatibility_matrix:
            avg_alignment = statistics.mean(compatibility_matrix.values())
        else:
            avg_alignment = 0.5

        # Priority synchronization (how well priorities align)
        priority_sync = avg_alignment * 0.8  # 80% weight on direct alignment

        # Add contextual factors
        shared_values_count = len(set(profile1_values.keys()) & set(profile2_values.keys()))
        contextual_bonus = min(shared_values_count * 0.1, 0.3)  # Up to 30% bonus for shared priorities

        final_alignment = min(1.0, priority_sync + contextual_bonus)

        return {
            "core_values_alignment": final_alignment,
            "priority_synchronization": priority_sync,
            "value_compatibility_matrix": compatibility_matrix,
            "shared_values_bonus": contextual_bonus,
            "alignment_factors": len(compatibility_matrix)
        }

    # ============================================================================
    # LEGACY COMPATIBILITY: Emulate expected method names
    # ============================================================================

    calculate_multidimensional_compatibility = calculate_multidimensional_compatibility
    assess_values_compatibility = assess_values_compatibility
