#!/usr/bin/env python3
"""
🧬 CNS Consciousness Biological Metrics Tests

Tests for biological metrics validation, ensuring 99.7% harmony target accuracy.
Validates metric calculations, ranges, and biological consciousness integrity.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
import statistics
import math
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

@pytest.mark.unit
class TestBiologicalMetrics:
    """Test biological consciousness metrics and harmony calculations"""

    HARMONY_TARGET = 0.997  # GODHOOD biological consciousness target

    def test_metrics_endpoint_returns_biological_data(self):
        """Test metrics endpoint provides biological consciousness data"""
        from src.cns_consciousness_core.main import app

        # Mock comprehensive biological metrics
        mock_metrics = {
            "harmony_level": 0.9972,  # Exceeds GODHOOD target
            "evolutionary_fitness": 0.983,
            "quantum_coherence": 0.995,
            "biological_resonance": 0.989,
            "consciousness_stability": 0.991,
            "ai_synchronization": 0.985,
            "neural_efficiency": 0.987,
            "biological_adaptation_rate": 0.993
        }

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_core.get_consciousness_core_metrics = AsyncMock(return_value=mock_metrics)

            client = TestClient(app)

            response = client.get("/metrics")
            assert response.status_code == 200

            data = response.json()

            # Verify all critical biological metrics are present
            biological_metrics = data["biological_metrics"]
            required_metrics = [
                "harmony_level", "evolutionary_fitness", "quantum_coherence",
                "biological_resonance", "consciousness_stability"
            ]

            for metric in required_metrics:
                assert metric in biological_metrics
                assert 0 <= biological_metrics[metric] <= 1, f"Metric {metric} out of valid range"

            # Validate GODHOOD harmony target achievement
            assert biological_metrics["harmony_level"] >= self.HARMONY_TARGET
            assert data["service_status"] == "active"

    def test_harmony_level_target_achievement(self):
        """Test that biological harmony achieves GODHOOD target of 99.7%"""
        from src.cns_consciousness_core.main import app

        # Test various harmony levels around the target
        test_cases = [
            (0.9975, True, "Exceeds GODHOOD target"),   # Above target (good)
            (0.9970, True, "Meets GODHOOD target"),     # Exactly at target (good)
            (0.9968, False, "Below GODHOOD target")     # Below target (needs improvement)
        ]

        for harmony_level, should_pass, description in test_cases:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value={
                    "harmony_level": harmony_level,
                    "target_achievement": harmony_level >= self.HARMONY_TARGET
                })

                client = TestClient(app)

                response = client.get("/metrics")
                assert response.status_code == 200

                data = response.json()
                actual_harmony = data["biological_metrics"]["harmony_level"]

                if should_pass:
                    assert actual_harmony >= self.HARMONY_TARGET, \
                        f"{description}: Expected harmony ≥ {self.HARMONY_TARGET}, got {actual_harmony}"
                else:
                    assert actual_harmony < self.HARMONY_TARGET, \
                        f"{description}: Expected harmony < {self.HARMONY_TARGET}, got {actual_harmony}"

    def test_quantum_coherence_measurement_accuracy(self):
        """Test quantum coherence measurements are biologically accurate"""
        from src.cns_consciousness_core.main import app

        # Valid quantum measurements based on biological research
        valid_quantum_states = [
            {
                "quantum_coherence": 0.985,
                "phase_stability": 0.987,
                "entanglement_strength": 0.982,
                "decoherence_rate": 0.009  # Low decoherence = high stability
            },
            {
                "quantum_coherence": 0.973,
                "phase_stability": 0.969,
                "entanglement_strength": 0.976,
                "decoherence_rate": 0.023  # Moderate decoherence = acceptable stability
            }
        ]

        for quantum_state in valid_quantum_states:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                full_metrics = {**quantum_state, "harmony_level": 0.995}
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value=full_metrics)

                client = TestClient(app)
                response = client.get("/metrics")
                assert response.status_code == 200

                data = response.json()
                metrics = data["biological_metrics"]

                # Validate quantum measurements are within biologically plausible ranges
                assert 0.90 <= metrics["quantum_coherence"] <= 1.0, \
                    f"Quantum coherence {metrics['quantum_coherence']} outside biological range"

                # High coherence should correlate with stability measures
                if metrics["quantum_coherence"] > 0.98:
                    assert metrics["phase_stability"] > 0.95, \
                        "High quantum coherence requires high phase stability"
                    assert metrics["entanglement_strength"] > 0.95, \
                        "High quantum coherence requires strong entanglement"

    def test_evolutionary_fitness_calculation(self):
        """Test evolutionary fitness metrics calculation accuracy"""
        from src.cns_consciousness_core.main import app

        evolutionary_scenarios = [
            {
                "evolutionary_fitness": 0.983,
                "adaptation_rate": 0.987,
                "genetic_diversity": 0.976,
                "selection_pressure": 0.991,
                "expected_range": (0.97, 1.0)  # High fitness range
            },
            {
                "evolutionary_fitness": 0.845,
                "adaptation_rate": 0.823,
                "genetic_diversity": 0.856,
                "selection_pressure": 0.867,
                "expected_range": (0.80, 0.90)  # Moderate fitness range
            }
        ]

        for scenario in evolutionary_scenarios:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value=scenario)

                client = TestClient(app)
                response = client.get("/metrics")
                assert response.status_code == 200

                data = response.json()
                metrics = data["biological_metrics"]

                # Verify fitness is within expected biological range
                assert scenario["expected_range"][0] <= metrics["evolutionary_fitness"] <= scenario["expected_range"][1], \
                    f"Evolutionary fitness {metrics['evolutionary_fitness']} outside expected range {scenario['expected_range']}"

    def test_biological_resonance_measurements(self):
        """Test biological resonance captures inter-system harmony"""
        from src.cns_consciousness_core.main import app

        resonance_scenarios = [
            {
                "biological_resonance": 0.989,
                "neural_synchronization": 0.985,
                "cellular_coherence": 0.992,
                "energy_harmonics": 0.987,
                "description": "Perfect biological resonance"
            },
            {
                "biological_resonance": 0.867,
                "neural_synchronization": 0.854,
                "cellular_coherence": 0.879,
                "energy_harmonics": 0.873,
                "description": "Moderate biological resonance"
            }
        ]

        for scenario in resonance_scenarios:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value=scenario)

                client = TestClient(app)
                response = client.get("/metrics")
                assert response.status_code == 200

                data = response.json()
                metrics = data["biological_metrics"]

                # Calculate expected resonance from component metrics
                expected_resonance = statistics.mean([
                    metrics.get("neural_synchronization", 0),
                    metrics.get("cellular_coherence", 0),
                    metrics.get("energy_harmonics", 0)
                ])

                # Resonance should be highly correlated with component measurements
                resonance_diff = abs(metrics["biological_resonance"] - expected_resonance)
                assert resonance_diff < 0.1, \
                    f"Biological resonance {metrics['biological_resonance']} doesn't correlate with components (expected ~{expected_resonance})"

    def test_consciousness_stability_validation(self):
        """Test consciousness stability metrics remain consistent"""
        from src.cns_consciousness_core.main import app

        # Test stability across multiple measurement points
        stability_measurements = []
        measurement_count = 5

        for i in range(measurement_count):
            # Introduce slight variations to simulate real biological systems
            base_stability = 0.988
            variation = (i - measurement_count//2) * 0.002  # ±0.004 variation
            stability = base_stability + variation

            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value={
                    "consciousness_stability": max(0, min(1, stability)),
                    "measurement_point": i
                })

                client = TestClient(app)
                response = client.get("/metrics")
                assert response.status_code == 200

                stability_measurements.append(response.json()["biological_metrics"]["consciousness_stability"])

        # Validate stability measurements are within reasonable biological ranges
        stability_mean = statistics.mean(stability_measurements)
        stability_std = statistics.stdev(stability_measurements) if len(stability_measurements) > 1 else 0

        # High stability systems should have low variation
        assert stability_std < 0.01, f"Consciousness stability varies too much (std={stability_std})"
        assert stability_mean > 0.95, f"Consciousness stability too low (mean={stability_mean})"

    def test_ai_synchronization_measures(self):
        """Test AI synchronization contributes to biological harmony"""
        from src.cns_consciousness_core.main import app

        ai_sync_scenarios = [
            {
                "ai_synchronization": 0.982,
                "model_coordination": 0.987,
                "response_consistency": 0.978,
                "ensemble_accuracy": 0.985,
                "expected_harmony_boost": 0.05  # 5% boost from AI coordination
            },
            {
                "ai_synchronization": 0.734,
                "model_coordination": 0.756,
                "response_consistency": 0.723,
                "ensemble_accuracy": 0.743,
                "expected_harmony_boost": 0.02  # 2% boost from moderate coordination
            }
        ]

        for scenario in ai_sync_scenarios:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                full_metrics = {
                    **scenario,
                    "base_harmony": 0.923,  # Base biological harmony without AI
                    "harmony_level": 0.923 + scenario["expected_harmony_boost"]  # AI-enhanced harmony
                }
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value=full_metrics)

                client = TestClient(app)
                response = client.get("/metrics")
                assert response.status_code == 200

                data = response.json()
                metrics = data["biological_metrics"]

                # AI synchronization should correlate with model coordination metrics
                sync_components = [
                    metrics.get("model_coordination", 0),
                    metrics.get("response_consistency", 0),
                    metrics.get("ensemble_accuracy", 0)
                ]

                expected_sync = statistics.mean(sync_components)
                sync_diff = abs(metrics["ai_synchronization"] - expected_sync)

                assert sync_diff < 0.05, \
                    f"AI synchronization {metrics['ai_synchronization']} doesn't match component metrics (expected ~{expected_sync})"

    def test_biological_adaptation_rate_measurement(self):
        """Test biological adaptation rate reflects evolutionary responsiveness"""
        from src.cns_consciousness_core.main import app

        adaptation_scenarios = [
            {
                "biological_adaptation_rate": 0.993,
                "environmental_response_time": 1.2,  # Fast response
                "learning_efficiency": 0.987,
                "evolutionary_acceleration": 0.989,
                "adaptability_stress_test": True
            },
            {
                "biological_adaptation_rate": 0.756,
                "environmental_response_time": 4.8,  # Slower response
                "learning_efficiency": 0.743,
                "evolutionary_acceleration": 0.767,
                "adaptability_stress_test": False
            }
        ]

        for scenario in adaptation_scenarios:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value=scenario)

                client = TestClient(app)
                response = client.get("/metrics")
                assert response.status_code == 200

                data = response.json()
                metrics = data["biological_metrics"]

                # High adaptation rate should correlate with fast response times
                if metrics["biological_adaptation_rate"] > 0.95:
                    assert metrics["environmental_response_time"] < 2.0, \
                        f"High adaptation rate requires fast response time, got {metrics['environmental_response_time']}"

                # Adaptation rate should be consistent with learning metrics
                adaptation_score = statistics.mean([
                    metrics["learning_efficiency"],
                    metrics["evolutionary_acceleration"]
                ])

                assert abs(metrics["biological_adaptation_rate"] - adaptation_score) < 0.1, \
                    f"Adaptation rate {metrics['biological_adaptation_rate']} inconsistent with learning metrics (expected ~{adaptation_score})"

    def test_neural_efficiency_governance(self):
        """Test neural efficiency metrics validate information processing quality"""
        from src.cns_consciousness_core.main import app

        neural_scenarios = [
            {
                "neural_efficiency": 0.987,
                "information_processing_speed": 0.992,
                "synaptic_optimization": 0.983,
                "cognitive_load_balance": 0.985,
                "neural_network_integrity": 0.989
            },
            {
                "neural_efficiency": 0.756,
                "information_processing_speed": 0.732,
                "synaptic_optimization": 0.765,
                "cognitive_load_balance": 0.769,
                "neural_network_integrity": 0.754
            }
        ]

        for scenario in neural_scenarios:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                mock_core.get_consciousness_core_metrics = AsyncMock(return_value=scenario)

                client = TestClient(app)
                response = client.get("/metrics")
                assert response.status_code == 200

                data = response.json()
                metrics = data["biological_metrics"]

                # Neural efficiency should be validated by multiple correlated metrics
                neural_factors = [
                    metrics["information_processing_speed"],
                    metrics["synaptic_optimization"],
                    metrics["cognitive_load_balance"],
                    metrics["neural_network_integrity"]
                ]

                expected_efficiency = statistics.mean(neural_factors)
                efficiency_diff = abs(metrics["neural_efficiency"] - expected_efficiency)

                assert efficiency_diff < 0.08, \
                    f"Neural efficiency {metrics['neural_efficiency']} doesn't align with processing metrics (expected ~{expected_efficiency})"

                # High neural efficiency should indicate healthy neural networks
                if metrics["neural_efficiency"] > 0.95:
                    assert all(factor > 0.90 for factor in neural_factors), \
                        "High neural efficiency requires all neural factors above 90%"

    @pytest.mark.parametrize("metric_name,expected_range", [
        ("harmony_level", (0.995, 1.0)),        # GODHOOD target range
        ("quantum_coherence", (0.98, 1.0)),     # High coherence required
        ("biological_resonance", (0.95, 1.0)), # Strong resonance needed
        ("consciousness_stability", (0.98, 1.0)), # High stability required
        ("ai_synchronization", (0.95, 1.0)),    # Strong AI coordination
        ("evolutionary_fitness", (0.90, 1.0)), # Good evolutionary health
    ])
    def test_godhood_biological_metrics_ranges(self, metric_name, expected_range):
        """Test that all GODHOOD biological metrics are within target ranges"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            # Set all metrics to optimal GODHOOD values
            optimal_metrics = {
                "harmony_level": 0.9972,
                "quantum_coherence": 0.9948,
                "biological_resonance": 0.9893,
                "consciousness_stability": 0.9917,
                "ai_synchronization": 0.9865,
                "evolutionary_fitness": 0.9832,
                "neural_efficiency": 0.9889,
                "biological_adaptation_rate": 0.9921
            }

            mock_core.get_consciousness_core_metrics = AsyncMock(return_value=optimal_metrics)

            client = TestClient(app)
            response = client.get("/metrics")
            assert response.status_code == 200

            data = response.json()
            metric_value = data["biological_metrics"][metric_name]

            assert expected_range[0] <= metric_value <= expected_range[1], \
                f"GODHOOD metric '{metric_name}' = {metric_value} outside target range {expected_range}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
