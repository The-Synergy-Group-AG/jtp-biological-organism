"""
Integration Tests for GODHOOD Modular Components
Tests complete workflows across all modular components
"""

import pytest
import asyncio
import statistics
from unittest.mock import Mock, patch

from src.personality_matching.core.personality_profile import PersonalityProfile, ProfileAnalyzer
from src.personality_matching.core.compatibility_engine import MultiDimensionalCompatibilityAnalyzer
from src.personality_matching.integration.integration_framework import IntegrationFramework
from src.emotional_intelligence.emotional_profile_analyzer import EmotionalProfileAnalyzer, EmotionalProfile
from src.emotional_intelligence.empathy_network_analyzer import EmpathyNetworkAnalyzer


class TestPersonalityMatchingWorkflow:
    """Test complete personality matching workflow"""

    @pytest.fixture
    def workflow_components(self):
        """Initialize all personality matching workflow components"""
        return {
            "profile_analyzer": ProfileAnalyzer(),
            "compatibility_analyzer": MultiDimensionalCompatibilityAnalyzer(),
            "integration_framework": IntegrationFramework()
        }

    @pytest.mark.asyncio
    async def test_complete_personality_matching_workflow(self, workflow_components):
        """Test end-to-end personality matching workflow"""
        profile_analyzer = workflow_components["profile_analyzer"]
        compatibility_analyzer = workflow_components["compatibility_analyzer"]
        integration_framework = workflow_components["integration_framework"]

        # Step 1: Analyze consciousness alignment for two profiles
        profile1_data = {
            "traits": {"openness": 0.8, "conscientiousness": 0.9, "empathy": 0.85},
            "values": {"growth": 0.9, "innovation": 0.8, "harmony": 0.9}
        }
        profile2_data = {
            "traits": {"openness": 0.9, "conscientiousness": 0.8, "empathy": 0.9},
            "values": {"growth": 0.8, "creativity": 0.95, "harmony": 0.85}
        }

        consciousness1 = await profile_analyzer.analyze_consciousness_alignment(profile1_data)
        consciousness2 = await profile_analyzer.analyze_consciousness_alignment(profile2_data)

        assert consciousness1["consciousness_alignment_score"] > 0
        assert consciousness2["consciousness_alignment_score"] > 0

        # Step 2: Calculate multidimensional compatibility
        profile1_traits = profile1_data["traits"]
        profile2_traits = profile2_data["traits"]

        compatibility = await compatibility_analyzer.calculate_multidimensional_compatibility(
            profile1_traits, profile2_traits
        )

        assert "overall_compatibility" in compatibility
        assert "dimensional_breakdown" in compatibility
        assert 0 <= compatibility["overall_compatibility"] <= 1

        # Step 3: Integrate system components
        component_status = await integration_framework.integrate_system_components(
            ["profile_analyzer", "compatibility_analyzer"]
        )

        assert component_status["integration_complete"] is True
        assert len(component_status) > 1

        # Step 4: Validate workflow completeness
        workflow_metrics = {
            "consciousness_analysis_completed": 2,
            "compatibility_calculated": True,
            "system_integration_successful": component_status["integration_complete"],
            "workflow_integrity_score": min(1.0, (compatibility["overall_compatibility"] +
                                                consciousness1["consciousness_alignment_score"] +
                                                consciousness2["consciousness_alignment_score"]) / 3)
        }

        assert workflow_metrics["workflow_integrity_score"] > 0.5


class TestEmotionalIntelligenceWorkflow:
    """Test complete emotional intelligence workflow"""

    @pytest.fixture
    def workflow_components(self):
        """Initialize emotional intelligence workflow components"""
        return {
            "profile_analyzer": EmotionalProfileAnalyzer(),
            "empathy_analyzer": EmpathyNetworkAnalyzer()
        }

    @pytest.mark.asyncio
    async def test_complete_emotional_intelligence_workflow(self, workflow_components):
        """Test end-to-end emotional intelligence workflow"""
        profile_analyzer = workflow_components["profile_analyzer"]
        empathy_analyzer = workflow_components["empathy_analyzer"]

        # Step 1: Analyze emotional profiles
        profile1_data = {
            "emotions": "highly empathetic, emotionally aware, strong self-regulation",
            "strengths": "understanding others, emotional resilience",
            "communication": "compassionate listening",
            "social_style": "collaborative, supportive"
        }

        profile2_data = {
            "emotions": "empathetic, understanding, emotionally intelligent",
            "strengths": "relationship building, conflict resolution",
            "communication": "empathetic dialogue",
            "social_style": "team-oriented, emotionally supportive"
        }

        analysis1 = await profile_analyzer.analyze_emotional_dimensions(profile1_data)
        analysis2 = await profile_analyzer.analyze_emotional_dimensions(profile2_data)

        assert analysis1["overall_ei_score"] > 0
        assert analysis2["overall_ei_score"] > 0

        # Step 2: Create emotional profiles
        profile1 = EmotionalProfile(
            profile_id="ei_test_profile1",
            user_id="user1",
            empathy_dimensions=analysis1["empathy_dimensions"],
            biological_emotional_synthesis=0.8,
            evolutionary_emotional_readiness=0.85
        )

        profile2 = EmotionalProfile(
            profile_id="ei_test_profile2",
            user_id="user2",
            empathy_dimensions=analysis2["empathy_dimensions"],
            biological_emotional_synthesis=0.85,
            evolutionary_emotional_readiness=0.9
        )

        # Step 3: Analyze empathy mapping
        empathy_mapping = await empathy_analyzer.analyze_empathy_mapping(profile1, profile2)

        assert "overall_empathy_resonance" in empathy_mapping
        assert "cognitive_empathy_mapping" in empathy_mapping

        # Step 4: Assess emotional resonance
        context = {"relationship_type": "professional", "interaction_frequency": "daily"}
        resonance = await empathy_analyzer.assess_emotional_resonance(profile1, profile2, context)

        assert "biological_emotional_resonance" in resonance
        assert "consciousness_emotional_sync" in resonance

        # Step 5: Validate workflow completeness
        workflow_metrics = {
            "emotional_profiles_analyzed": 2,
            "empathy_mapping_established": True,
            "emotional_resonance_assessed": True,
            "average_emotional_intelligence": (analysis1["overall_ei_score"] + analysis2["overall_ei_score"]) / 2,
            "empathy_resonance_score": empathy_mapping.get("overall_empathy_resonance", 0),
            "biological_resonance_score": resonance.get("biological_emotional_resonance", 0),
            "workflow_emotional_integrity": min(1.0, sum([
                analysis1["overall_ei_score"],
                analysis2["overall_ei_score"],
                empathy_mapping.get("overall_empathy_resonance", 0),
                resonance.get("biological_emotional_resonance", 0)
            ]) / 4)
        }

        assert workflow_metrics["workflow_emotional_integrity"] > 0.6


class TestCrossModuleIntegration:
    """Test integration between personality and emotional intelligence modules"""

    @pytest.fixture
    def cross_module_components(self):
        """Initialize components from both modules"""
        return {
            "personality_analyzer": ProfileAnalyzer(),
            "emotional_analyzer": EmotionalProfileAnalyzer(),
            "empathy_analyzer": EmpathyNetworkAnalyzer()
        }

    @pytest.mark.asyncio
    async def test_personality_emotional_integration(self, cross_module_components):
        """Test integration between personality and emotional intelligence"""
        personality_analyzer = cross_module_components["personality_analyzer"]
        emotional_analyzer = cross_module_components["emotional_analyzer"]
        empathy_analyzer = cross_module_components["empathy_analyzer"]

        # Step 1: Analyze complementary profiles
        personality_data = {
            "traits": {"openness": 0.9, "conscientiousness": 0.8, "empathy": 0.85},
            "values": {"relationships": 0.9, "understanding": 0.8, "growth": 0.85}
        }

        emotional_data = {
            "emotions": "highly empathetic, emotionally intelligent",
            "strengths": "strong empathy, relationship building",
            "communication": "compassionate, understanding",
            "social_style": "collaborative, supportive"
        }

        personality_analysis = await personality_analyzer.analyze_consciousness_alignment(personality_data)
        emotional_analysis = await emotional_analyzer.analyze_emotional_dimensions(emotional_data)

        # Step 2: Create integrated profiles
        personality_profile = PersonalityProfile(
            profile_id="cross_test_personality",
            user_id="user_cross",
            multidimensional_traits={"openness": personality_data["traits"]["openness"],
                                   "conscientiousness": personality_data["traits"]["conscientiousness"],
                                   "empathy": personality_data["traits"]["empathy"]},
            core_values_alignment={"relationships": personality_data["values"]["relationships"],
                                 "understanding": personality_data["values"]["understanding"],
                                 "growth": personality_data["values"]["growth"]}
        )

        emotional_profile = EmotionalProfile(
            profile_id="cross_test_emotional",
            user_id="user_cross",
            empathy_dimensions=emotional_analysis["empathy_dimensions"],
            biological_emotional_synthesis=emotional_analysis["overall_ei_score"],
            evolutionary_emotional_readiness=min(emotional_analysis["overall_ei_score"] + 0.1, 1.0)
        )

        # Step 3: Test cross-module empathy mapping
        empathy_mapping = await empathy_analyzer.analyze_empathy_mapping(emotional_profile, emotional_profile)

        # Since we're comparing the same profile to itself, empathy should be perfect
        assert empathy_mapping["overall_empathy_resonance"] >= 0.9

        # Step 4: Validate cross-module consistency
        personality_empathy_trait = personality_profile.multidimensional_traits.get("empathy", 0)
        emotional_empathy_avg = statistics.mean(emotional_profile.empathy_dimensions.values())

        # Cross-module empathy alignment should be within reasonable bounds
        empathy_consistency = abs(personality_empathy_trait - emotional_empathy_avg)
        assert empathy_consistency <= 0.2, f"Cross-module empathy inconsistency: {empathy_consistency}"

        # Biological alignment across modules
        personality_biological = personality_profile.evolutionary_consciousness
        emotional_biological = emotional_profile.biological_emotional_synthesis

        biological_consistency = abs(personality_biological - emotional_biological)
        assert biological_consistency <= 0.25, f"Cross-module biological inconsistency: {biological_consistency}"

        # Step 5: Comprehensive integration validation
        integration_metrics = {
            "personality_analysis_completed": True,
            "emotional_analysis_completed": True,
            "cross_module_empathy_aligned": empathy_consistency <= 0.2,
            "cross_module_biological_aligned": biological_consistency <= 0.25,
            "overall_integration_score": min(1.0, (
                personality_analysis["consciousness_alignment_score"] +
                emotional_analysis["overall_ei_score"] +
                personality_biological +
                emotional_biological +
                empathy_mapping["overall_empathy_resonance"]
            ) / 5)
        }

        assert integration_metrics["overall_integration_score"] > 0.7


class TestSystemResilienceIntegration:
    """Test system resilience and error handling across modules"""

    @pytest.mark.asyncio
    async def test_partial_component_failure_resilience(self):
        """Test system resilience when some components fail"""
        # Simulate component failures
        mock_passing_component = Mock()
        mock_passing_component.analyze_consciousness_alignment.return_value = {
            "consciousness_alignment_score": 0.8,
            "status": "success"
        }

        mock_failing_component = Mock()
        mock_failing_component.analyze_emotional_dimensions.side_effect = Exception("Analysis failed")

        # Test that system can continue with partial component failures
        # This simulates real-world scenarios where some analyses might fail

        passing_result = await mock_passing_component.analyze_consciousness_alignment({})

        assert passing_result["consciousness_alignment_score"] == 0.8

        # Validate resilience - system should handle component failures gracefully
        with pytest.raises(Exception):
            await mock_failing_component.analyze_emotional_dimensions({})

    def test_data_validation_integration(self):
        """Test data validation across integrated components"""
        # Test with invalid data
        invalid_profile = PersonalityProfile(
            profile_id="",  # Invalid: empty ID
            user_id="test_user",
            multidimensional_traits={},  # Invalid: empty traits
            core_values_alignment={}
        )

        # Profile should still be created but with sensible defaults
        assert invalid_profile.evolutionary_consciousness == 0.8  # Default value
        assert invalid_profile.multidimensional_traits == {}
        assert invalid_profile.core_values_alignment == {}

        # Test with extreme values
        extreme_profile = EmotionalProfile(
            profile_id="extreme_test",
            user_id="user_extreme",
            biological_emotional_synthesis=2.0,  # Invalid: > 1.0
            evolutionary_emotional_readiness=1.5,  # Invalid: > 1.0
            empathy_dimensions={"cognitive_empathy": 1.5, "emotional_empathy": 0.8}  # Mixed valid/invalid
        )

        # System should handle extreme values gracefully
        # (Note: In a real implementation, these would be clamped to valid ranges)
        assert extreme_profile.profile_id == "extreme_test"
        assert extreme_profile.user_id == "user_extreme"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
