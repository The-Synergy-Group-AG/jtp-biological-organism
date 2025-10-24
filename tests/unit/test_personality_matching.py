"""
Unit Tests for Personality Matching Modular Components
Tests all 7 personality-matching modules independently
"""

import pytest
import asyncio
import statistics
from unittest.mock import Mock, patch

from src.personality_matching.core.personality_profile import PersonalityProfile, ProfileAnalyzer
from src.personality_matching.core.compatibility_engine import MultiDimensionalCompatibilityAnalyzer
from src.personality_matching.core.intelligence_engine import PersonalityProfileAnalyzer
from src.personality_matching.integration.integration_framework import IntegrationFramework
from src.personality_matching.integration.strategy_engine import StrategyEngine
from src.personality_matching.optimization.consciousness_optimizer import ConsciousnessOptimizer, EvolutionaryPersonalityMetrics


class TestPersonalityProfile:
    """Test PersonalityProfile class"""

    def test_personality_profile_creation(self):
        """Test basic personality profile creation"""
        profile = PersonalityProfile(profile_id="test_123", user_id="user_test")
        assert profile.profile_id == "test_123"
        assert profile.user_id == "user_test"
        assert profile.multidimensional_traits == {}
        assert profile.core_values_alignment == {}
        assert profile.evolutionary_consciousness == 0.8

    def test_personality_profile_with_traits(self):
        """Test personality profile with predefined traits"""
        traits = {"openness": 0.8, "conscientiousness": 0.9}
        values = {"growth": 0.7, "innovation": 0.8}

        profile = PersonalityProfile(
            profile_id="test_123",
            user_id="user_test",
            multidimensional_traits=traits,
            core_values_alignment=values
        )

        assert profile.multidimensional_traits["openness"] == 0.8
        assert profile.core_values_alignment["growth"] == 0.7

    def test_get_compatibility_dimensions(self):
        """Test compatibility dimensions retrieval"""
        profile = PersonalityProfile(profile_id="test_123", user_id="user_test")
        dimensions = profile.get_compatibility_dimensions()

        assert isinstance(dimensions, dict)
        assert "multidimensional_traits" in dimensions
        assert "core_values_alignment" in dimensions
        assert "evolutionary_consciousness" in dimensions


class TestProfileAnalyzer:
    """Test ProfileAnalyzer functionality"""

    @pytest.fixture
    def analyzer(self):
        """Create ProfileAnalyzer instance"""
        return ProfileAnalyzer()

    def test_analyzer_initialization(self, analyzer):
        """Test ProfileAnalyzer initialization"""
        assert analyzer is not None
        assert hasattr(analyzer, 'analyze_consciousness_alignment')
        assert hasattr(analyzer, 'calculate_evolutionary_readiness')

    @pytest.mark.asyncio
    async def test_consciousness_alignment_analysis(self, analyzer):
        """Test consciousness alignment analysis"""
        test_data = {
            "traits": {"openness": 0.8, "conscientiousness": 0.7},
            "values": {"growth": 0.9, "innovation": 0.8}
        }

        result = await analyzer.analyze_consciousness_alignment(test_data)

        assert isinstance(result, dict)
        assert "consciousness_alignment_score" in result
        assert "evolutionary_readiness" in result
        assert result["consciousness_alignment_score"] >= 0.0
        assert result["consciousness_alignment_score"] <= 1.0

    @pytest.mark.asyncio
    async def test_evolutionary_readiness_calculation(self, analyzer):
        """Test evolutionary readiness calculation"""
        traits = {"openness": 0.8, "adaptation": 0.9}
        consciousness_context = {"evolutionary_stage": "conscious"}

        readiness = await analyzer.calculate_evolutionary_readiness(traits, consciousness_context)

        assert isinstance(readiness, float)
        assert readiness >= 0.0
        assert readiness <= 1.0


class TestMultiDimensionalCompatibilityAnalyzer:
    """Test compatibility analysis engine"""

    @pytest.fixture
    def compatibility_analyzer(self):
        """Create compatibility analyzer instance"""
        return MultiDimensionalCompatibilityAnalyzer()

    def test_analyzer_initialization(self, compatibility_analyzer):
        """Test analyzer initialization"""
        assert compatibility_analyzer is not None
        assert hasattr(compatibility_analyzer, 'calculate_multidimensional_compatibility')
        assert hasattr(compatibility_analyzer, 'assess_values_compatibility')

    @pytest.mark.asyncio
    async def test_multidimensional_compatibility(self, compatibility_analyzer):
        """Test multidimensional compatibility calculation"""
        profile1_traits = {"openness": 0.8, "conscientiousness": 0.7}
        profile2_traits = {"openness": 0.9, "conscientiousness": 0.6}

        compatibility = await compatibility_analyzer.calculate_multidimensional_compatibility(
            profile1_traits, profile2_traits
        )

        assert isinstance(compatibility, dict)
        assert "overall_compatibility" in compatibility
        assert "dimensional_breakdown" in compatibility

    @pytest.mark.asyncio
    async def test_values_compatibility(self, compatibility_analyzer):
        """Test values compatibility assessment"""
        profile1_values = {"growth": 0.8, "innovation": 0.9}
        profile2_values = {"growth": 0.7, "innovation": 0.8}

        compatibility = await compatibility_analyzer.assess_values_compatibility(
            profile1_values, profile2_values
        )

        assert isinstance(compatibility, dict)
        assert "core_values_alignment" in compatibility
        assert "priority_synchronization" in compatibility


class TestPersonalityProfileAnalyzer:
    """Test personality intelligence analysis"""

    @pytest.fixture
    def intelligence_analyzer(self):
        """Create intelligence analyzer instance"""
        return PersonalityProfileAnalyzer()

    @pytest.mark.asyncio
    async def test_profile_analysis(self, intelligence_analyzer):
        """Test comprehensive profile analysis"""
        profile_data = {
            "traits": {"openness": 0.8, "conscientiousness": 0.9},
            "values": {"growth": 0.7},
            "behavior_patterns": ["collaborative", "innovative"]
        }

        analysis = await intelligence_analyzer.analyze_personality_profile(profile_data)

        assert isinstance(analysis, dict)
        assert "personality_insights" in analysis
        assert "strengths_profile" in analysis
        assert "development_areas" in analysis


class TestIntegrationFramework:
    """Test integration framework"""

    @pytest.fixture
    def integration_framework(self):
        """Create integration framework instance"""
        return IntegrationFramework()

    @pytest.mark.asyncio
    async def test_profile_integration(self, integration_framework):
        """Test profile integration capabilities"""
        profiles = ["profile1", "profile2"]

        integration = await integration_framework.integrate_personality_profiles(profiles)

        assert isinstance(integration, dict)
        assert "integration_status" in integration
        assert "unified_profile" in integration

    @pytest.mark.asyncio
    async def test_system_integration(self, integration_framework):
        """Test system-level integration"""
        components = ["compatibility", "intelligence", "optimization"]

        status = await integration_framework.integrate_system_components(components)

        assert isinstance(status, dict)
        assert "integration_complete" in status


class TestStrategyEngine:
    """Test strategy engine functionality"""

    @pytest.fixture
    def strategy_engine(self):
        """Create strategy engine instance"""
        return StrategyEngine()

    @pytest.mark.asyncio
    async def test_strategy_development(self, strategy_engine):
        """Test strategy development"""
        analysis_data = {
            "compatibility_scores": {"professional": 0.8, "personal": 0.6},
            "risk_factors": ["communication_gaps"],
            "opportunities": ["collaboration_potential"]
        }

        strategy = await strategy_engine.develop_matching_strategy(analysis_data)

        assert isinstance(strategy, dict)
        assert "strategy_type" in strategy
        assert "implementation_plan" in strategy

    @pytest.mark.asyncio
    async def test_strategy_evaluation(self, strategy_engine):
        """Test strategy evaluation"""
        strategy_plan = {
            "approach": "balanced_integration",
            "timeline": "3_months"
        }

        evaluation = await strategy_engine.evaluate_strategy_effectiveness(strategy_plan)

        assert isinstance(evaluation, dict)
        assert "effectiveness_score" in evaluation


class TestConsciousnessOptimizer:
    """Test consciousness optimization engine"""

    @pytest.fixture
    def consciousness_optimizer(self):
        """Create consciousness optimizer instance"""
        return ConsciousnessOptimizer()

    @pytest.mark.asyncio
    async def test_optimization_cycle(self, consciousness_optimizer):
        """Test optimization cycle execution"""
        current_metrics = EvolutionaryPersonalityMetrics()

        optimization = await consciousness_optimizer.run_optimization_cycle(current_metrics)

        assert isinstance(optimization, dict)
        assert "optimization_complete" in optimization
        assert "improvement_metrics" in optimization

    @pytest.mark.asyncio
    async def test_evolutionary_adaptation(self, consciousness_optimizer):
        """Test evolutionary adaptation"""
        adaptation_context = {
            "environmental_changes": ["market_volatility"],
            "adaptive_requirements": ["flexibility", "resilience"]
        }

        adaptation = await consciousness_optimizer.adapt_to_evolutionary_changes(adaptation_context)

        assert isinstance(adaptation, dict)
        assert "adaptation_strategies" in adaptation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
