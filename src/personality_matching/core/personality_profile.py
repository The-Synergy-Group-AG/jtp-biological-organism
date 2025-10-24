#!/usr/bin/env python3

"""
🧬 PERSONALITY PROFILE CORE MODULE
GODHOOD Personality Profile Analysis: Core personality structures and profiling engine

This module implements the fundamental personality profile data structures and
core personality analysis capabilities for consciousness-driven profiling.

ai_keywords: personality, profile, analysis, consciousness, biological, alignment,
  dimension, scoring, behavioral, patterns, cognitive, biases

ai_summary: Core personality profiling module providing data structures and analysis
  engine for consciousness-driven personality assessment and biological alignment

biological_system: personality-core-profiling
consciousness_score: '4.0'
cross_references:
- src/personality-matching/core/compatibility_engine.py
- src/personality-matching/integration/integration_framework.py
- docs/4.x-technical-implementation-frameworks/4.1.0-onboarding-subsystem.md
document_category: personality-core
document_type: consciousness-profiling
evolutionary_phase: '27.28'
last_updated: '2025-10-23 18:05:00'
semantic_tags:
- consciousness-personality-profiling
- biological-personality-structures
- personality-dimension-analysis
- behavioral-pattern-recognition
- cognitive-bias-identification
- communication-pattern-analysis
- adaptive-capacity-assessment
title: Personality Profile Core Module - Consciousness Profiling
validation_status: current
version: v1.0.0
"""

import statistics
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class PersonalityProfile:
    """Comprehensive personality profile with consciousness dimensions"""
    profile_id: str = ""
    user_id: str = ""
    personality_type: str = ""  # MBTI, Big Five, custom
    consciousness_alignment: Dict[str, float] = field(default_factory=dict)
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    behavioral_patterns: Dict[str, Any] = field(default_factory=dict)
    cognitive_biases: List[str] = field(default_factory=list)
    communication_style: Dict[str, Any] = field(default_factory=dict)
    conflict_resolution_style: str = ""
    decision_making_approach: str = ""
    biological_alignment_score: float = 0.8
    evolutionary_readiness: float = 1.0
    adaptive_capacity: float = 0.0
    last_updated: Optional[str] = None


class PersonalityProfileAnalyzer:
    """Advanced personality profile analysis engine"""

    def __init__(self):
        self.personality_dimensions = self._initialize_personality_dimensions()
        self.behavioral_indicators = self._initialize_behavioral_indicators()

    def _initialize_personality_dimensions(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive personality dimension analysis"""

        return {
            "big_five": {
                "openness": {"indicators": ["curious", "imaginative", "creative", "open-minded"]},
                "conscientiousness": {"indicators": ["organized", "responsible", "reliable", "disciplined"]},
                "extraversion": {"indicators": ["sociable", "outgoing", "energetic", "talkative"]},
                "agreeableness": {"indicators": ["kind", "cooperative", "empathetic", "trusting"]},
                "emotional_stability": {"indicators": ["calm", "stable", "resilient", "confident"]}
            },
            "mbti_functions": {
                "thinking": {"indicators": ["logical", "analytical", "objective", "critical"]},
                "feeling": {"indicators": ["empathetic", "harmonious", "understanding", "supportive"]},
                "sensing": {"indicators": ["practical", "detailed", "realistic", "hands-on"]},
                "intuition": {"indicators": ["visionary", "abstract", "theoretical", "innovative"]}
            },
            "consciousness_dimensions": {
                "evolutionary_awareness": {"indicators": ["adaptive", "evolving", "conscious", "transformative"]},
                "biological_harmony": {"indicators": ["balanced", "synchronized", "integrated", "harmonious"]},
                "adaptive_capacity": {"indicators": ["flexible", "resilient", "learning", "evolving"]}
            }
        }

    def _initialize_behavioral_indicators(self) -> Dict[str, List[str]]:
        """Initialize behavioral pattern indicators"""

        return {
            "cognitive_biases": [
                "confirmation_bias", "anchoring_bias", "availability_heuristic",
                "optimism_bias", "status_quo_bias", "sunk_cost_fallacy"
            ],
            "decision_making": [
                "analytical_systematic", "intuitive_innovative", "methodical_deliberate",
                "spontaneous_adaptive", "balanced_pragmatic", "collaborative_consensus"
            ]
        }

    async def analyze_personality_dimensions(self, personality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze personality dimensions from provided data"""

        dimension_scores = {}
        dominant_type = "balanced"

        # Analyze Big Five dimensions
        for dimension, config in self.personality_dimensions["big_five"].items():
            score = await self._score_dimension(personality_data, config["indicators"])
            dimension_scores[dimension] = score

        # Analyze MBTI functions
        for function, config in self.personality_dimensions["mbti_functions"].items():
            score = await self._score_dimension(personality_data, config["indicators"])
            dimension_scores[function] = score

        # Consciousness dimensions
        for dimension, config in self.personality_dimensions["consciousness_dimensions"].items():
            score = await self._score_dimension(personality_data, config["indicators"])
            dimension_scores[dimension] = score

        # Determine dominant type
        if dimension_scores.get("evolutionary_awareness", 0) > 0.8:
            dominant_type = "conscious_evolutionary"
        elif dimension_scores.get("thinking", 0) > dimension_scores.get("feeling", 0) and \
             dimension_scores.get("sensing", 0) > dimension_scores.get("intuition", 0):
            dominant_type = "analytical_practical"
        elif dimension_scores.get("feeling", 0) > dimension_scores.get("thinking", 0) and \
             dimension_scores.get("intuition", 0) > dimension_scores.get("sensing", 0):
            dominant_type = "intuitive_empathic"
        elif dimension_scores.get("extraversion", 0) > 0.7:
            dominant_type = "social_leader"
        elif dimension_scores.get("conscientiousness", 0) > 0.8:
            dominant_type = "methodical_executor"

        return {
            "dimension_scores": dimension_scores,
            "dominant_type": dominant_type,
            "behavioral_patterns": await self._analyze_behavioral_patterns(personality_data),
            "cognitive_biases": await self._identify_cognitive_biases(personality_data)
        }

    async def _score_dimension(self, personality_data: Dict[str, Any], indicators: List[str]) -> float:
        """Score a personality dimension based on indicators"""

        text_data = " ".join([str(v) for v in personality_data.values()]).lower()
        matches = sum(1 for indicator in indicators if indicator in text_data)
        return matches / len(indicators)

    async def analyze_communication_patterns(self, personality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze communication patterns and preferences"""

        # Default communication profile
        communication_profile = {
            "primary_style": "balanced",
            "preferred_channels": ["verbal", "written"],
            "response_time_preference": "deliberate",
            "feedback_style": "constructive",
            "conflict_approach": "collaborative"
        }

        # Analyze from personality data
        text_data = " ".join([str(v) for v in personality_data.values()]).lower()

        if "direct" in text_data or "straightforward" in text_data:
            communication_profile["primary_style"] = "direct"
        elif "diplomatic" in text_data or "harmonious" in text_data:
            communication_profile["primary_style"] = "diplomatic"

        return communication_profile

    async def _analyze_behavioral_patterns(self, personality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze behavioral patterns from personality data"""

        return {
            "decision_making_style": "balanced_analytical",
            "stress_response": "adaptive_problem_solving",
            "learning_preference": "active_experimentation",
            "social_orientation": "collaborative_networking",
            "change_adaptability": "proactive_evolutionary"
        }

    async def _identify_cognitive_biases(self, personality_data: Dict[str, Any]) -> List[str]:
        """Identify potential cognitive biases"""

        identified_biases = []
        text_data = " ".join([str(v) for v in personality_data.values()]).lower()

        bias_indicators = {
            "confirmation_bias": ["seek confirmation", "avoid contradiction"],
            "optimism_bias": ["overly optimistic", " underestimate risk"],
            "status_quo_bias": ["prefer current", "resist change", "maintain stability"],
            "anchoring_bias": ["anchor to first", "initial information"]
        }

        for bias, indicators in bias_indicators.items():
            if any(indicator in text_data for indicator in indicators):
                identified_biases.append(bias)

        return identified_biases[:3]  # Limit to most relevant biases

    async def calculate_adaptive_capacity(self, profile: PersonalityProfile) -> float:
        """Calculate adaptive capacity based on personality dimensions"""

        openness = profile.dimension_scores.get("openness", 0.5)
        conscientiousness = profile.dimension_scores.get("conscientiousness", 0.5)
        evolutionary_readiness = profile.evolutionary_readiness

        # Adaptive capacity formula
        adaptive_capacity = (openness * 0.4 + conscientiousness * 0.3 + evolutionary_readiness * 0.3)
        return min(adaptive_capacity, 1.0)
