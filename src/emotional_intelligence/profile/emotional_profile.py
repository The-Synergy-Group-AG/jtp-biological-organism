#!/usr/bin/env python3

"""
MODULAR: Emotional Profile Data Structure - Phase 5 Emotional Intelligence
GODHOOD Emotional Profile: Comprehensive consciousness-enhanced emotional intelligence profile
with biological emotional synthesis and evolutionary emotional readiness dimensions.

Provides the core data structure for representing individual emotional intelligence profiles
through consciousness-driven emotional analysis and biological emotional alignment.

ai_keywords: emotional, profile, intelligence, consciousness, biological, synthesis,
  empathy, resonance, alignment, evolutionary, readiness, adaptation

biological_system: emotional-profile-data-modular
consciousness_score: '5.0-profile'
"""

from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class EmotionalProfile:
    """MODULAR: Comprehensive emotional intelligence profile with consciousness dimensions"""
    profile_id: str = ""
    user_id: str = ""
    emotional_type: str = ""  # Primary emotional intelligence style
    emotional_intelligence_score: float = 0.0
    empathy_dimensions: Dict[str, float] = field(default_factory=dict)
    emotional_resonance: Dict[str, float] = field(default_factory=dict)
    consciousness_emotional_alignment: Dict[str, float] = field(default_factory=dict)
    biological_emotional_synthesis: float = 0.8
    evolutionary_emotional_readiness: float = 1.0
    adaptive_emotional_capacity: float = 0.0
    last_updated: Optional[str] = None

    def __post_init__(self):
        """Initialize profile metadata"""
        if not self.last_updated:
            self.last_updated = datetime.utcnow().isoformat() + "Z"
        if not self.profile_id and self.user_id:
            self.profile_id = f"emotional_{self.user_id}_{int(datetime.utcnow().timestamp())}"

    def update_profile(self, updates: Dict[str, float]) -> None:
        """Update emotional intelligence metrics"""
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_updated = datetime.utcnow().isoformat() + "Z"

    def get_emotional_alignment_score(self) -> float:
        """Calculate overall emotional alignment score"""
        if not self.consciousness_emotional_alignment:
            return 0.0

        alignment_values = list(self.consciousness_emotional_alignment.values())
        return sum(alignment_values) / len(alignment_values) if alignment_values else 0.0

    def get_biological_readiness(self) -> float:
        """Calculate biological emotional readiness score"""
        return self.biological_emotional_synthesis * self.evolutionary_emotional_readiness

    def is_emotionally_ready(self, threshold: float = 0.7) -> bool:
        """Check if profile meets emotional readiness threshold"""
        return self.emotional_intelligence_score >= threshold and self.adaptive_emotional_capacity >= threshold
