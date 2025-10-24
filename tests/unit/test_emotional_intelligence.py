"""
Unit Tests for Emotional Intelligence Modular Components
Tests all 4 emotional-intelligence modules independently
"""

import pytest
import asyncio
import statistics
from unittest.mock import Mock, patch

from src.emotional_intelligence.emotional_profile_analyzer import EmotionalProfileAnalyzer, EmotionalProfile
from src.emotional_intelligence.empathy_network_analyzer import EmpathyNetworkAnalyzer, EmpathyNetwork
from src.emotional_intelligence.emotional_synthesis_framework import EmotionalSynthesisFramework
from src.emotional_intelligence.consciousness_emotional_optimization import ConsciousnessEmotionalOptimizationEngine


class TestEmotionalProfileAnalyzer:
    """Test EmotionalProfileAnalyzer functionality"""

    @pytest.fixture
    def analyzer(self):
        """Create EmotionalProfileAnalyzer instance"""
        return EmotionalProfileAnalyzer()

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization"""
        assert analyzer is not None
        assert hasattr(analyzer, 'analyze_emotional_dimensions')
        assert hasattr(analyzer, 'assess_empathetic_capacity')

    @pytest.mark.asyncio
    async def test_emotional_dimensions_analysis(self, analyzer):
        """Test emotional dimensions analysis"""
        emotional_data = {
            "emotions": "empathetic, self-aware, emotionally intelligent",
            "strengths": "understanding others, emotional resilience",
            "communication": "compassionate listening",
            "social_style": "collaborative, supportive"
        }

        analysis = await analyzer.analyze_emotional_dimensions(emotional_data)

        assert isinstance(analysis, dict)
        assert "overall_ei_score" in analysis
        assert "dominant_emotional_type" in analysis
        assert "empathy_dimensions" in analysis
        assert 0.0 <= analysis["overall_ei_score"] <= 1.0

    @pytest.mark.asyncio
    async def test_empathetic_capacity_assessment(self, analyzer):
        """Test empathetic capacity assessment"""
        empathy_indicators = {
            "cognitive_empathy": 0.8,
            "emotional_empathy": 0.9
        }

        capacity = await analyzer.assess_empathetic_capacity(empathy_indicators)

        assert isinstance(capacity, float)
        assert 0.0 <= capacity <= 1.0

    @pytest.mark.asyncio
    async def test_biological_emotional_synthesis(self, analyzer):
        """Test biological emotional synthesis calculation"""
        profile_analysis = {
            "overall_ei_score": 0.8,
            "empathy_dimensions": {"cognitive_empathy": 0.9, "emotional_empathy": 0.7}
        }

        synthesis_score = await analyzer.calculate_biological_emotional_synthesis(profile_analysis)

        assert isinstance(synthesis_score, float)
        assert 0.0 <= synthesis_score <= 1.0


class TestEmpathyNetworkAnalyzer:
    """Test EmpathyNetworkAnalyzer functionality"""

    @pytest.fixture
    def analyzer(self):
        """Create EmpathyNetworkAnalyzer instance"""
        return EmpathyNetworkAnalyzer()

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization"""
        assert analyzer is not None
        assert hasattr(analyzer, 'analyze_empathy_mapping')
        assert hasattr(analyzer, 'assess_emotional_resonance')

    @pytest.mark.asyncio
    async def test_empathy_mapping_analysis(self, analyzer):
        """Test empathy mapping between emotional profiles"""
        profile1 = EmotionalProfile(
            profile_id="profile1",
            empathy_dimensions={"cognitive_empathy": 0.8, "emotional_empathy": 0.7}
        )
        profile2 = EmotionalProfile(
            profile_id="profile2",
            empathy_dimensions={"cognitive_empathy": 0.9, "emotional_empathy": 0.6}
        )

        mapping = await analyzer.analyze_empathy_mapping(profile1, profile2)

        assert isinstance(mapping, dict)
        assert "overall_empathy_resonance" in mapping
        assert "cognitive_empathy_mapping" in mapping
        assert "emotional_empathy_mapping" in mapping

    @pytest.mark.asyncio
    async def test_emotional_resonance_assessment(self, analyzer):
        """Test emotional resonance assessment"""
        profile1 = EmotionalProfile(
            profile_id="profile1",
            biological_emotional_synthesis=0.8
        )
        profile2 = EmotionalProfile(
            profile_id="profile2",
            biological_emotional_synthesis=0.9
        )
        context = {"relationship_type": "professional"}

        resonance = await analyzer.assess_emotional_resonance(profile1, profile2, context)

        assert isinstance(resonance, dict)
        assert "biological_emotional_resonance" in resonance
        assert "consciousness_emotional_sync" in resonance
        assert "relationship_harmonic_potential" in resonance

    @pytest.mark.asyncio
    async def test_relationship_optimization(self, analyzer):
        """Test relationship optimization potential"""
        profile1 = EmotionalProfile(
            profile_id="profile1",
            empathy_dimensions={"cognitive_empathy": 0.8}
        )
        profile2 = EmotionalProfile(
            profile_id="profile2",
            empathy_dimensions={"cognitive_empathy": 0.7}
        )

        optimization = await analyzer.evaluate_relationship_optimization(profile1, profile2)

        assert isinstance(optimization, float)
        assert 0.0 <= optimization <= 1.0

    @pytest.mark.asyncio
    async def test_emotional_conflict_resolution(self, analyzer):
        """Test emotional conflict resolution assessment"""
        profile1 = EmotionalProfile(
            profile_id="profile1",
            emotional_intelligence_score=0.8
        )
        profile2 = EmotionalProfile(
            profile_id="profile2",
            emotional_intelligence_score=0.9
        )
        context = {"situation_intensity": "moderate"}

        resolution = await analyzer.assess_emotional_conflict_resolution(profile1, profile2, context)

        assert isinstance(resolution, float)
        assert 0.0 <= resolution <= 1.0

    @pytest.mark.asyncio
    async def test_collaboration_synergy(self, analyzer):
        """Test collaboration emotional synergy"""
        profile1 = EmotionalProfile(
            profile_id="profile1",
            empathy_dimensions={"cognitive_empathy": 0.8},
            biological_emotional_synthesis=0.8
        )
        profile2 = EmotionalProfile(
            profile_id="profile2",
            empathy_dimensions={"emotional_empathy": 0.9},
            biological_emotional_synthesis=0.9
        )
        context = {"collaboration_type": "team_work"}

        synergy = await analyzer.evaluate_collaboration_synergy(profile1, profile2, context)

        assert isinstance(synergy, float)
        assert 0.0 <= synergy <= 1.0


class TestEmotionalSynthesisFramework:
    """Test EmotionalSynthesisFramework functionality"""

    @pytest.fixture
    def framework(self):
        """Create EmotionalSynthesisFramework instance"""
        return EmotionalSynthesisFramework()

    def test_framework_initialization(self, framework):
        """Test framework initialization"""
        assert framework is not None
        assert hasattr(framework, 'define_emotional_objectives')
        assert hasattr(framework, 'develop_synthesis_strategy')

    @pytest.mark.asyncio
    async def test_emotional_objectives_definition(self, framework):
        """Test emotional objectives definition"""
        profile_ids = ["profile1", "profile2", "profile3"]
        synthesis_context = {"type": "team", "duration": "6_months"}

        objectives = await framework.define_emotional_objectives(profile_ids, synthesis_context)

        assert isinstance(objectives, list)
        assert len(objectives) > 0
        assert any("team" in obj.lower() for obj in objectives)

    @pytest.mark.asyncio
    async def test_synthesis_strategy_development(self, framework):
        """Test synthesis strategy development"""
        profiles = [
            EmotionalProfile(profile_id="profile1", empathy_dimensions={"cognitive_empathy": 0.8}),
            EmotionalProfile(profile_id="profile2", empathy_dimensions={"emotional_empathy": 0.9})
        ]
        synthesis_context = {"type": "professional"}

        strategy = await framework.develop_synthesis_strategy(profiles, synthesis_context)

        assert isinstance(strategy, dict)
        assert "synthesis_approach" in strategy
        assert "empathy_amplification_plan" in strategy
        assert "emotional_resonance_network" in strategy

    @pytest.mark.asyncio
    async def test_empathy_protocols_optimization(self, framework):
        """Test empathy network protocols optimization"""
        synthesis = Mock()
        synthesis.participant_profiles = ["p1", "p2", "p3"]
        synthesis_context = {"type": "team"}

        protocols = await framework.optimize_empathy_protocols(synthesis, synthesis_context)

        assert isinstance(protocols, dict)
        assert "empathy_sharing_channels" in protocols
        assert "resonance_frequency_optimization" in protocols

    @pytest.mark.asyncio
    async def test_emotional_conflict_framework_creation(self, framework):
        """Test emotional conflict resolution framework"""
        synthesis = Mock()
        synthesis.participant_profiles = ["p1", "p2"]
        synthesis_context = {"type": "professional"}

        conflict_framework = await framework.create_emotional_conflict_framework(synthesis, synthesis_context)

        assert isinstance(conflict_framework, dict)
        assert "primary_emotional_approach" in conflict_framework
        assert "escalation_emotional_levels" in conflict_framework


class TestConsciousnessEmotionalOptimizationEngine:
    """Test ConsciousnessEmotionalOptimizationEngine functionality"""

    @pytest.fixture
    def optimizer(self):
        """Create optimizer instance"""
        return ConsciousnessEmotionalOptimizationEngine()

    def test_optimizer_initialization(self, optimizer):
        """Test optimizer initialization"""
        assert optimizer is not None
        assert hasattr(optimizer, 'establish_emotional_goals')
        assert hasattr(optimizer, 'assess_current_emotional_state')

    @pytest.mark.asyncio
    async def test_emotional_goals_establishment(self, optimizer):
        """Test emotional goals establishment"""
        target_profiles = ["profile1", "profile2"]
        optimization_context = {"optimization_type": "team_emotional_intelligence"}

        goals = await optimizer.establish_emotional_goals(target_profiles, optimization_context)

        assert isinstance(goals, list)
        assert len(goals) > 0
        assert any("team" in goal.lower() for goal in goals)

    @pytest.mark.asyncio
    async def test_emotional_state_assessment(self, optimizer):
        """Test current emotional state assessment"""
        profiles = [
            EmotionalProfile(profile_id="p1", biological_emotional_synthesis=0.8,
                           evolutionary_emotional_readiness=0.9, emotional_intelligence_score=0.7),
            EmotionalProfile(profile_id="p2", biological_emotional_synthesis=0.9,
                           evolutionary_emotional_readiness=0.8, emotional_intelligence_score=0.8)
        ]

        assessment = await optimizer.assess_current_emotional_state(profiles)

        assert isinstance(assessment, dict)
        assert "average_emotional_harmony" in assessment
        assert "biological_emotional_alignment" in assessment
        assert "evolutionary_emotional_readiness" in assessment
        assert "empathy_coherence" in assessment

    @pytest.mark.asyncio
    async def test_emotional_pathways_identification(self, optimizer):
        """Test emotional pathways identification"""
        optimization = Mock()
        optimization_context = {"focus_area": "empathy_enhancement"}

        pathways = await optimizer.identify_emotional_pathways(optimization, optimization_context)

        assert isinstance(pathways, list)
        assert len(pathways) > 0
        assert all(isinstance(pathway, dict) for pathway in pathways)

    @pytest.mark.asyncio
    async def test_biological_emotional_targets_calculation(self, optimizer):
        """Test biological emotional targets calculation"""
        optimization = Mock()
        optimization.current_emotional_state_assessment = {
            "biological_emotional_alignment": 0.7,
            "evolutionary_emotional_readiness": 0.8,
            "empathy_coherence": 0.6,
            "emotional_adaptive_capacity_distribution": [0.7, 0.8]
        }

        targets = await optimizer.calculate_biological_emotional_targets(optimization)

        assert isinstance(targets, dict)
        assert "biological_emotional_harmony_target" in targets
        assert "evolutionary_emotional_readiness_target" in targets
        assert "empathy_coherence_target" in targets

    @pytest.mark.asyncio
    async def test_emotional_strategies_development(self, optimizer):
        """Test consciousness emotional strategies development"""
        optimization = Mock()
        optimization_context = {"strategy_type": "harmonization"}

        strategies = await optimizer.develop_consciousness_emotional_strategies(optimization, optimization_context)

        assert isinstance(strategies, dict)
        assert "biological_emotional_harmonization" in strategies
        assert "evolutionary_emotional_acceleration" in strategies
        assert "empathy_optimization" in strategies


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
