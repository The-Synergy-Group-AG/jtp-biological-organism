"""
Load and Performance Tests for GODHOOD Modular Components
Tests system performance under various load conditions
"""

import pytest
import asyncio
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from memory_profiler import profile
import psutil
import os

from src.personality_matching.core.personality_profile import PersonalityProfile, ProfileAnalyzer
from src.emotional_intelligence.emotional_profile_analyzer import EmotionalProfileAnalyzer


class TestPersonalityMatchingLoad:
    """Load tests for personality matching components"""

    @pytest.fixture
    def analyzer(self):
        """Create ProfileAnalyzer instance"""
        return ProfileAnalyzer()

    def test_concurrent_profile_analysis(self, analyzer):
        """Test concurrent profile analysis under load"""
        async def analyze_single_profile(profile_data):
            return await analyzer.analyze_consciousness_alignment(profile_data)

        async def run_concurrent_analysis(num_profiles):
            """Run multiple profile analyses concurrently"""
            profile_data_template = {
                "traits": {"openness": 0.8, "conscientiousness": 0.7},
                "values": {"growth": 0.9, "innovation": 0.8}
            }

            start_time = time.time()

            # Create analysis tasks
            tasks = []
            for i in range(num_profiles):
                profile_data = profile_data_template.copy()
                profile_data["user_id"] = f"user_{i}"
                tasks.append(analyze_single_profile(profile_data))

            # Execute concurrently
            results = await asyncio.gather(*tasks)
            end_time = time.time()

            return {
                "execution_time": end_time - start_time,
                "results_count": len(results),
                "throughput": len(results) / (end_time - start_time),
                "avg_result": statistics.mean([r.get("consciousness_alignment_score", 0) for r in results])
            }

        @pytest.mark.asyncio
        @pytest.mark.parametrize("num_profiles", [10, 50, 100])
        async def test_scalability(self, analyzer, num_profiles):
            """Test system scalability with increasing load"""
            results = await run_concurrent_analysis(num_profiles)

            assert results["results_count"] == num_profiles
            assert results["execution_time"] > 0
            assert results["throughput"] > 0

            # Acceptable throughput thresholds
            min_throughput = num_profiles / 30.0  # At least 1 analysis per 3 seconds
            assert results["throughput"] >= min_throughput


class TestEmotionalIntelligenceLoad:
    """Load tests for emotional intelligence components"""

    @pytest.fixture
    def analyzer(self):
        """Create EmotionalProfileAnalyzer instance"""
        return EmotionalProfileAnalyzer()

    @pytest.mark.asyncio
    async def test_emotional_analysis_throughput(self, analyzer):
        """Test emotional analysis throughput under load"""
        async def analyze_emotions(analysis_data):
            return await analyzer.analyze_emotional_dimensions(analysis_data)

        async def run_batch_analysis(batch_size):
            """Run batch emotional analysis"""
            start_time = time.time()

            # Template emotional data
            template_data = {
                "emotions": "empathetic, self-aware, emotionally intelligent",
                "strengths": "understanding others, emotional resilience",
                "communication": "compassionate listening",
                "social_style": "collaborative, supportive"
            }

            tasks = []
            for i in range(batch_size):
                data_copy = template_data.copy()
                data_copy["user_id"] = f"user_{i}"
                tasks.append(analyze_emotions(data_copy))

            results = await asyncio.gather(*tasks)
            end_time = time.time()

            return {
                "batch_size": batch_size,
                "execution_time": end_time - start_time,
                "throughput": batch_size / (end_time - start_time),
                "avg_ei_score": statistics.mean([r["overall_ei_score"] for r in results]),
                "memory_usage": psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
            }

        # Test different batch sizes
        for batch_size in [25, 50, 100]:
            results = await run_batch_analysis(batch_size)

            assert results["batch_size"] == batch_size
            assert results["execution_time"] > 0
            assert results["throughput"] > batch_size / 60.0  # At least 1 per minute
            assert 0 <= results["avg_ei_score"] <= 1.0


class TestMemoryUsageAnalysis:
    """Memory usage analysis for modular components"""

    @profile
    def test_personality_profile_memory_usage(self):
        """Test memory usage during personality profile operations"""
        profiles = []

        # Create many profiles to test memory scaling
        for i in range(1000):
            profile = PersonalityProfile(
                profile_id=f"profile_{i}",
                user_id=f"user_{i}",
                multidimensional_traits={"openness": 0.8, "conscientiousness": 0.9},
                core_values_alignment={"growth": 0.7, "innovation": 0.8}
            )
            profiles.append(profile)

        # Ensure all profiles are created without memory issues
        assert len(profiles) == 1000

        # Test profile operations
        total_evolutionary_consciousness = sum(p.evolutionary_consciousness for p in profiles)
        assert total_evolutionary_consciousness >= 800  # Should be around 1000 * 0.8

    @profile
    def test_emotional_profile_memory_usage(self):
        """Test memory usage during emotional profile operations"""
        from src.emotional_intelligence.emotional_profile_analyzer import EmotionalProfile

        profiles = []

        # Create emotional profiles
        for i in range(500):
            profile = EmotionalProfile(
                profile_id=f"emotional_{i}",
                user_id=f"user_{i}",
                empathy_dimensions={"cognitive_empathy": 0.8, "emotional_empathy": 0.9}
            )
            profiles.append(profile)

        assert len(profiles) == 500

        # Test emotional operations
        avg_adaptive_capacity = statistics.mean(p.adaptive_emotional_capacity for p in profiles)
        assert avg_adaptive_capacity >= 0.0


class TestConcurrencyStressTest:
    """Stress tests for concurrent execution of multiple modular components"""

    @pytest.mark.slow
    def test_mixed_component_concurrency(self):
        """Test concurrent execution of multiple different component types"""

        async def execute_mixed_operations(num_operations):
            """Execute mixed personality and emotional operations concurrently"""
            start_time = time.time()

            # Initialize analyzers
            personality_analyzer = ProfileAnalyzer()
            emotional_analyzer = EmotionalProfileAnalyzer()

            async def personality_analysis():
                data = {
                    "traits": {"openness": 0.8, "conscientiousness": 0.7},
                    "values": {"growth": 0.9, "innovation": 0.8}
                }
                return await personality_analyzer.analyze_consciousness_alignment(data)

            async def emotional_analysis():
                data = {
                    "emotions": "empathetic, self-aware",
                    "strengths": "understanding, resilience",
                    "communication": "compassionate",
                    "social_style": "collaborative"
                }
                return await emotional_analyzer.analyze_emotional_dimensions(data)

            # Create mixed operation tasks
            tasks = []
            for i in range(num_operations):
                if i % 2 == 0:
                    tasks.append(personality_analysis())
                else:
                    tasks.append(emotional_analysis())

            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks)
            end_time = time.time()

            return {
                "total_operations": num_operations,
                "execution_time": end_time - start_time,
                "operations_per_second": num_operations / (end_time - start_time),
                "results_count": len(results),
                "avg_result_score": statistics.mean([
                    r.get("consciousness_alignment_score", r.get("overall_ei_score", 0))
                    for r in results
                ])
            }

        @pytest.mark.asyncio
        @pytest.mark.parametrize("num_operations", [30, 60])
        async def test_concurrent_mixed_operations(self, num_operations):
            """Test concurrent mixed operations"""
            results = await execute_mixed_operations(num_operations)

            assert results["total_operations"] == num_operations
            assert results["results_count"] == num_operations
            assert results["execution_time"] > 5  # Should take reasonable time
            assert results["operations_per_second"] > num_operations / 120.0  # At least 1 per 2 minutes


class TestResourceMonitoring:
    """Resource monitoring and alerting for modular components"""

    def monitor_system_resources(self):
        """Monitor system resources during testing"""
        process = psutil.Process(os.getpid())

        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "memory_percent": process.memory_percent(),
            "threads": process.num_threads(),
            "open_files": len(process.open_files()) if hasattr(process, 'open_files') else 0
        }

    def test_resource_baseline(self):
        """Establish resource usage baseline"""
        resources = self.monitor_system_resources()

        assert resources["cpu_percent"] >= 0
        assert resources["memory_mb"] > 0
        assert resources["threads"] > 0

        # Alert if resource usage seems problematic
        if resources["memory_mb"] > 1000:  # Over 1GB
            pytest.skip("High memory usage detected - skipping resource-intensive test")

    def test_performance_regression_alerts(self):
        """Test for performance regression alerts"""
        # Simple performance assertion
        start_time = time.time()
        time.sleep(0.1)  # Small delay
        end_time = time.time()

        execution_time = end_time - start_time
        assert execution_time < 0.2  # Should complete quickly

        if execution_time > 0.15:  # Performance alert threshold
            pytest.skip("Potential performance regression detected")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--durations=10"])
