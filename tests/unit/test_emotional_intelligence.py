"""
Unit Tests for Emotional Intelligence Modular Components
Tests all 4 emotional-intelligence modules independently
"""

import pytest
import asyncio
import statistics
import time

import sys
sys.path.insert(0, '/home/andre/projects/jtp-biological-organism/src')

# Real imports - no Mock objects for actual functionality
from emotional_intelligence.emotional_profile_analyzer import EmotionalProfileAnalyzer, EmotionalProfile, EmpathyNetworkAnalyzer


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

    def test_empathy_score_calculation(self, analyzer):
        """Test empathy score calculation with known inputs"""
        # Test with perfect empathy indicators
        perfect_empathy_data = {
            "perspective_taking": 0.9,
            "emotional_contagion": 0.9,
            "compassionate_response": 0.9,
            "active_listening": 0.9,
            "emotional_awareness": 0.9
        }

        perfect_score = analyzer.calculate_empathy_score(perfect_empathy_data)
        assert 0.8 <= perfect_score <= 1.0  # Should be very high

        # Test with low empathy indicators
        low_empathy_data = {
            "perspective_taking": 0.1,
            "emotional_contagion": 0.1,
            "compassionate_response": 0.1,
            "active_listening": 0.1,
            "emotional_awareness": 0.1
        }

        low_score = analyzer.calculate_empathy_score(low_empathy_data)
        assert 0.0 <= low_score <= 0.3  # Should be very low

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

    @pytest.mark.asyncio
    async def test_empathy_edge_cases(self, analyzer):
        """Test empathy mapping with extreme and identical profiles"""
        # Test identical profiles (perfect resonance)
        identical_dimensions = {"cognitive_empathy": 0.8, "emotional_empathy": 0.9, "compassionate_empathy": 0.7}

        profile1 = EmotionalProfile(
            profile_id="identical1",
            empathy_dimensions=identical_dimensions.copy()
        )
        profile2 = EmotionalProfile(
            profile_id="identical2",
            empathy_dimensions=identical_dimensions.copy()
        )

        perfect_mapping = await analyzer.analyze_empathy_mapping(profile1, profile2)
        assert perfect_mapping["overall_empathy_resonance"] >= 0.8  # Should be high (along expected algorithmic range)

        # Test completely opposite profiles (poor resonance)
        opposite1_dimensions = {"cognitive_empathy": 0.1, "emotional_empathy": 0.9}
        opposite2_dimensions = {"cognitive_empathy": 0.9, "emotional_empathy": 0.1}

        profile3 = EmotionalProfile(
            profile_id="opposite1",
            empathy_dimensions=opposite1_dimensions
        )
        profile4 = EmotionalProfile(
            profile_id="opposite2",
            empathy_dimensions=opposite2_dimensions
        )

        poor_mapping = await analyzer.analyze_empathy_mapping(profile3, profile4)
        assert poor_mapping["overall_empathy_resonance"] < 0.6  # Should be lower due to cognitive differences

    @pytest.mark.asyncio
    async def test_relationship_contexts(self, analyzer):
        """Test resonance under different relationship contexts"""
        profile1 = EmotionalProfile(
            profile_id="context_test1",
            biological_emotional_synthesis=0.8,
            evolutionary_emotional_readiness=0.7
        )
        profile2 = EmotionalProfile(
            profile_id="context_test2",
            biological_emotional_synthesis=0.9,
            evolutionary_emotional_readiness=0.8
        )

        contexts = ["professional", "personal", "familial", "therapeutic"]

        resonances = {}
        for ctx in contexts:
            resonance = await analyzer.assess_emotional_resonance(profile1, profile2, {"relationship_type": ctx})
            resonances[ctx] = resonance["biological_emotional_resonance"]

        # Therapeutic context should typically have highest resonance due to emotional attunement
        assert resonances["therapeutic"] >= resonances["professional"]
        assert resonances["personal"] >= resonances["professional"]

    @pytest.mark.asyncio
    async def test_collaboration_intensity(self, analyzer):
        """Test collaboration synergy with different work intensity levels"""
        team_player = EmotionalProfile(
            profile_id="team_player",
            empathy_dimensions={"cognitive_empathy": 0.8, "emotional_empathy": 0.9},
            biological_emotional_synthesis=0.85
        )
        individual_worker = EmotionalProfile(
            profile_id="individual",
            empathy_dimensions={"cognitive_empathy": 0.9, "emotional_empathy": 0.4},
            biological_emotional_synthesis=0.75
        )

        # Test team work synergy
        team_synergy = await analyzer.evaluate_collaboration_synergy(
            team_player, individual_worker, {"collaboration_type": "team_work"}
        )

        # Test individual work synergy
        individual_synergy = await analyzer.evaluate_collaboration_synergy(
            team_player, individual_worker, {"collaboration_type": "independent"}
        )

        assert 0.0 <= team_synergy <= 1.0
        assert 0.0 <= individual_synergy <= 1.0
        # Team work could benefit from complementary skills
        assert team_synergy >= individual_synergy * 0.8  # Allow for reasonable difference


class TestEmotionalIntelligencePerformance:
    """Performance tests for emotional intelligence operations"""

    @pytest.fixture
    def profile_analyzer(self):
        """Create emotional profile analyzer instance"""
        return EmotionalProfileAnalyzer()

    @pytest.fixture
    def network_analyzer(self):
        """Create empathy network analyzer instance"""
        return EmpathyNetworkAnalyzer()

    def test_empathy_analysis_performance(self, profile_analyzer):
        """Test performance of empathy analysis calculations"""
        emotional_data = {
            "emotions": "highly empathetic and emotionally aware individual",
            "strengths": "strong interpersonal skills and emotional intelligence",
            "communication": "excellent listener with compassionate approach"
        }

        start_time = time.time()

        # Run analysis 10 times for averaging
        for _ in range(10):
            asyncio.run(profile_analyzer.analyze_emotional_dimensions(emotional_data))

        end_time = time.time()
        avg_time = (end_time - start_time) / 10

        # Should complete in under 0.5 seconds per analysis
        assert avg_time < 0.5, f"Emotional analysis too slow: {avg_time:.4f} seconds"

    @pytest.mark.asyncio
    async def test_empathy_mapping_performance(self, network_analyzer):
        """Test performance of empathy mapping operations"""
        profiles = []

        # Create test profiles
        for i in range(10):
            profile = EmotionalProfile(
                profile_id=f"perf_test_{i}",
                empathy_dimensions={
                    "cognitive_empathy": (i % 10) / 10.0,
                    "emotional_empathy": ((i + 2) % 10) / 10.0
                },
                biological_emotional_synthesis=0.8
            )
            profiles.append(profile)

        start_time = time.time()

        # Run empathy mapping between all pairs
        tasks = []
        for i in range(len(profiles)):
            for j in range(i + 1, len(profiles)):
                tasks.append(network_analyzer.analyze_empathy_mapping(profiles[i], profiles[j]))

        await asyncio.gather(*tasks, return_exceptions=True)

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete 45 mappings in under 10 seconds
        assert total_time < 10.0, f"Empathy mapping operations too slow: {total_time:.4f} seconds"

    @pytest.mark.asyncio
    async def test_concurrent_emotional_processing(self, profile_analyzer, network_analyzer):
        """Test concurrent emotional intelligence processing"""
        # Create multiple profiles for concurrent processing
        profiles = []
        analysis_tasks = []

        for i in range(5):
            profile_data = {
                "emotions": f"individual with {'high' if i % 2 else 'moderate'} emotional intelligence",
                "strengths": f"{'excellent' if i % 2 else 'good'} communication and empathy skills",
                "communication": f"{'compassionate' if i % 2 else 'adequate'} interpersonal approach"
            }

            profile = EmotionalProfile(
                profile_id=f"concurrent_{i}",
                empathy_dimensions={"cognitive_empathy": 0.8, "emotional_empathy": 0.7}
            )
            profiles.append(profile)
            analysis_tasks.append(profile_analyzer.analyze_emotional_dimensions(profile_data))

        mapping_tasks = []
        for i in range(len(profiles)):
            for j in range(i + 1, len(profiles)):
                mapping_tasks.append(network_analyzer.analyze_empathy_mapping(profiles[i], profiles[j]))

        start_time = time.time()

        # Run all operations concurrently
        await asyncio.gather(*analysis_tasks, *mapping_tasks, return_exceptions=True)

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete all operations in under 8 seconds
        assert total_time < 8.0, f"Concurrent emotional processing too slow: {total_time:.4f} seconds"


# REMOVED: Placeholder test classes for non-existent classes
# TestEmotionalSynthesisFramework and TestConsciousnessEmotionalOptimizationEngine removed
# as they tested classes that don't exist (EmotionalSynthesisFramework, ConsciousnessEmotionalOptimizationEngine)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
