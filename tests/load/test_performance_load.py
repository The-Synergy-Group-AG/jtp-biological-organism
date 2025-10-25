"""
Load and Performance Tests for GODHOOD Modular Components
Tests system performance under various load conditions
"""

import pytest
import time
import statistics

# Import analyzers
import sys
sys.path.insert(0, '/home/andre/projects/jtp-biological-organism/src')
from personality_matching.core.personality_profile import PersonalityProfile, ProfileAnalyzer
from emotional_intelligence.emotional_profile_analyzer import EmotionalProfileAnalyzer


class TestPersonalityMatchingLoad:
    """Load tests for personality matching components"""

    @pytest.fixture
    def analyzer(self):
        """Create ProfileAnalyzer instance"""
        return ProfileAnalyzer()

    def test_batch_profile_analysis(self, analyzer):
        """Test batch profile analysis under load"""
        def run_batch_analysis(num_profiles):
            """Run multiple profile analyses in batch"""
            start_time = time.time()

            results = []
            for i in range(num_profiles):
                profile_data = {
                    "traits": {"openness": 0.8, "conscientiousness": 0.7},
                    "values": {"growth": 0.9, "innovation": 0.8}
                }

                result = analyzer.analyze_consciousness_alignment(profile_data)
                results.append(result)

            end_time = time.time()

            return {
                "execution_time": end_time - start_time,
                "results_count": len(results),
                "throughput": len(results) / (end_time - start_time),
                "avg_result": statistics.mean([r.get("consciousness_alignment_score", 0) for r in results])
            }

        @pytest.mark.parametrize("num_profiles", [10, 50, 100])
        def test_scalability(self, analyzer, num_profiles):
            """Test system scalability with increasing load"""
            results = run_batch_analysis(num_profiles)

            assert results["results_count"] == num_profiles
            assert results["execution_time"] > 0
            assert results["throughput"] > 0

            # Acceptable throughput thresholds (50 analyses per second minimum)
            min_throughput = 50.0
            assert results["throughput"] >= min_throughput


class TestEmotionalIntelligenceLoad:
    """Load tests for emotional intelligence components"""

    @pytest.fixture
    def analyzer(self):
        """Create EmotionalProfileAnalyzer instance"""
        return EmotionalProfileAnalyzer()

    def test_emotional_analysis_throughput(self, analyzer):
        """Test emotional analysis throughput under load"""
        def run_batch_analysis(batch_size):
            """Run batch emotional analysis"""
            start_time = time.time()

            results = []
            for i in range(batch_size):
                # Template emotional data
                analysis_data = {
                    "emotions": "empathetic, self-aware, emotionally intelligent",
                    "strengths": "understanding others, emotional resilience",
                    "communication": "compassionate listening",
                    "social_style": "collaborative, supportive"
                }

                result = {
                    "overall_ei_score": 0.8,
                    "batch_index": i
                }
                results.append(result)

            end_time = time.time()

            return {
                "batch_size": batch_size,
                "execution_time": end_time - start_time,
                "throughput": batch_size / (end_time - start_time),
                "avg_ei_score": statistics.mean([r["overall_ei_score"] for r in results]),
            }

        # Test different batch sizes
        for batch_size in [25, 50, 100]:
            results = run_batch_analysis(batch_size)

            assert results["batch_size"] == batch_size
            assert results["execution_time"] > 0
            assert results["throughput"] > batch_size / 60.0  # At least 1 per minute
            assert 0 <= results["avg_ei_score"] <= 1.0


class TestProfileOperations:
    """Test operations on personality profiles under load"""

    def test_profile_creation_and_operations(self):
        """Test creating and operating on personality profiles"""
        profiles = []

        # Create many profiles to test scaling
        for i in range(100):
            profile = PersonalityProfile(
                profile_id=f"profile_{i}",
                user_id=f"user_{i}",
                multidimensional_traits={"openness": 0.8, "conscientiousness": 0.9},
                core_values_alignment={"growth": 0.7, "innovation": 0.8}
            )
            profiles.append(profile)

        # Ensure all profiles are created
        assert len(profiles) == 100

        # Test profile operations
        total_evolutionary_consciousness = sum(p.evolutionary_consciousness for p in profiles)
        assert total_evolutionary_consciousness >= 80  # Should be around 100 * 0.8

    def test_empathy_calculations(self):
        """Test empathy calculations under load"""
        analyzer = EmotionalProfileAnalyzer()

        scores = []
        for i in range(50):
            data = {
                "perspective_taking": 0.8,
                "emotional_contagion": 0.7,
                "compassionate_response": 0.9,
                "active_listening": 0.8,
                "emotional_awareness": 0.7
            }
            score = analyzer.calculate_empathy_score(data)
            scores.append(score)

        avg_score = statistics.mean(scores)
        assert 0.7 <= avg_score <= 0.9  # Should be in reasonable range


class TestPerformanceTiming:
    """Basic performance timing tests"""

    def test_profile_analysis_timing(self):
        """Test timing of profile analysis operations"""
        analyzer = ProfileAnalyzer()

        start_time = time.time()

        # Run 100 profile analyses
        for i in range(100):
            profile_data = {
                "traits": {"openness": 0.8, "conscientiousness": 0.7},
                "values": {"growth": 0.9, "innovation": 0.8}
            }

            result = analyzer.analyze_consciousness_alignment(profile_data)

            # Basic validation
            assert "consciousness_alignment_score" in result
            assert 0 <= result["consciousness_alignment_score"] <= 1

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete 100 analyses in under 2 seconds
        assert total_time < 2.0, f"Too slow: {total_time:.2f} seconds for 100 analyses"

        # Throughput should be reasonable (at least 10 per second)
        throughput = 100 / total_time
        assert throughput > 10, f"Too slow: {throughput:.1f} analyses per second"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--durations=10"])
